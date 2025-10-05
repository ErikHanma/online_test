from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Test, Question, Answer, TestResult, CodeSubmission, UserProfile
from .forms import CandidateRegistrationForm
import subprocess
import tempfile
import os


def test_list(request):
    """Список доступных тестов"""
    tests = Test.objects.filter(is_active=True)
    
    # Фильтрация по специализации если пользователь авторизован
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        user_specialization = request.user.profile.specialization
        # Показываем тесты соответствующей специализации
        recommended_tests = tests.filter(specialization=user_specialization)
        other_tests = tests.exclude(specialization=user_specialization)
        
        return render(request, 'myapp/test_list.html', {
            'recommended_tests': recommended_tests,
            'other_tests': other_tests,
            'user_specialization': user_specialization
        })
    
    return render(request, 'myapp/test_list.html', {'tests': tests})


def register(request):
    """Регистрация нового кандидата"""
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена! Добро пожаловать!')
            return redirect('test_list')
    else:
        form = CandidateRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})


@login_required
def profile(request):
    """Профиль пользователя с историей тестов"""
    results = TestResult.objects.filter(user=request.user).order_by('-timestamp')
    
    stats = {
        'total_tests': results.count(),
        'avg_score': 0,
        'best_score': 0
    }
    
    if results.exists():
        scores = [r.percentage_score for r in results]
        stats['avg_score'] = round(sum(scores) / len(scores), 1)
        stats['best_score'] = max(scores)
    
    return render(request, 'myapp/profile.html', {
        'results': results,
        'stats': stats
    })


@login_required
def test_detail(request, pk):
    """Страница прохождения теста"""
    test = get_object_or_404(Test, pk=pk, is_active=True)
    questions = test.questions.prefetch_related('answers').order_by('order', 'id')
    return render(request, 'myapp/test_detail.html', {
        'test': test,
        'questions': questions
    })


def execute_python_code(code, expected_output, timeout=5):
    """
    Безопасное выполнение Python кода
    Возвращает (output, is_correct, error)
    """
    temp_file = None
    try:
        # Создаем временный файл с явной UTF-8 кодировкой
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Выполняем код с ограничением времени
        result = subprocess.run(
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Удаляем временный файл
        os.unlink(temp_file)
        temp_file = None
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if error:
            return output, False, error
        
        # Проверяем соответствие ожидаемому результату
        is_correct = output == expected_output.strip()
        
        return output, is_correct, None
        
    except subprocess.TimeoutExpired:
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)
        return '', False, 'Превышено время выполнения'
    except Exception as e:
        if temp_file and os.path.exists(temp_file):
            os.unlink(temp_file)
        return '', False, str(e)


@login_required
def submit_test(request, pk):
    """Обработка отправки теста"""
    test = get_object_or_404(Test, pk=pk)
    
    if request.method != 'POST':
        return redirect('test_detail', pk=pk)
    
    score = 0
    questions = test.questions.all()
    total_questions = questions.count()
    
    # Создаем результат теста
    result = TestResult.objects.create(
        test=test,
        user=request.user,
        candidate_name=f"{request.user.first_name} {request.user.last_name}",
        score=0,
        total_questions=total_questions
    )
    
    # Обрабатываем ответы
    for question in questions:
        if question.question_type == 'single':
            submitted_answer_id = request.POST.get(f'question_{question.pk}')
            
            if submitted_answer_id:
                try:
                    submitted_answer = Answer.objects.get(pk=int(submitted_answer_id))
                    if submitted_answer.is_correct:
                        score += 1
                except (Answer.DoesNotExist, ValueError):
                    pass
        
        elif question.question_type == 'code':
            # Задача с кодом
            submitted_code = request.POST.get(f'code_{question.pk}', '')
            
            if submitted_code and question.expected_output:
                output, is_correct, error = execute_python_code(
                    submitted_code,
                    question.expected_output
                )
                
                # Сохраняем отправленный код
                CodeSubmission.objects.create(
                    result=result,
                    question=question,
                    code=submitted_code,
                    output=output if not error else f"ERROR: {error}",
                    is_correct=is_correct
                )
                
                if is_correct:
                    score += 1
    
    # Обновляем результат
    result.score = score
    result.save()
    
    messages.success(request, f'Тест завершен! Ваш результат: {score}/{total_questions}')
    return redirect('test_result', pk=test.pk, result_pk=result.pk)


@login_required
def test_result(request, pk, result_pk):
    """Страница результатов теста"""
    test = get_object_or_404(Test, pk=pk)
    result = get_object_or_404(TestResult, pk=result_pk, user=request.user)
    
    code_submissions = result.code_submissions.select_related('question').all()
    
    return render(request, 'myapp/test_result.html', {
        'test': test,
        'result': result,
        'code_submissions': code_submissions
    })
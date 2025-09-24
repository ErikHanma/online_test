from django.shortcuts import render, get_object_or_404, redirect
from .models import Test, Question, Answer, TestResult

def test_list(request):
    tests = Test.objects.all()
    return render(request, 'myapp/test_list.html', {'tests': tests})

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    questions = test.questions.all()
    return render(request, 'myapp/test_detail.html', {'test': test, 'questions': questions})

def submit_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        score = 0
        total_questions = test.questions.count()
        
        for question in test.questions.all():
            submitted_answer_id = request.POST.get(f'question_{question.pk}')
            
            if submitted_answer_id:
                try:
                    correct_answer = question.answers.get(is_correct=True)
                    if correct_answer.pk == int(submitted_answer_id):
                        score += 1
                except Answer.DoesNotExist:
                    continue

        result = TestResult.objects.create(
            test=test,
            score=score,
            total_questions=total_questions
        )
        
        return redirect('test_result', pk=test.pk, result_pk=result.pk)

    return redirect('test_detail', pk=test.pk)

def test_result(request, pk, result_pk):
    test = get_object_or_404(Test, pk=pk)
    result = get_object_or_404(TestResult, pk=result_pk)
    return render(request, 'myapp/test_result.html', {'test': test, 'result': result})
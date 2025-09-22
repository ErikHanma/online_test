from django.shortcuts import render, get_object_or_404
from .models import Test, Question

def test_list(request):
    tests = Test.objects.all()
    return render(request, 'myapp/test_list.html', {'tests': tests})

def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    questions = test.questions.all()
    return render(request, 'myapp/test_detail.html', {'test': test, 'questions': questions})
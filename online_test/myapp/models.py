from django.db import models

class Test(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание")
    specialization = models.CharField(
        max_length=50,
        choices=(('backend', 'Backend'), ('frontend', 'Frontend'), ('qa', 'QA')),
        default='backend',
        verbose_name="Специализация"
    )
    time_limit_minutes = models.IntegerField(default=60, verbose_name="Лимит времени (минуты)")

    def __str__(self):
        return self.title

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions', verbose_name="Тест")
    text = models.TextField(verbose_name="Текст вопроса")
    
    def __str__(self):
        return f"Вопрос для теста '{self.test.title}': {self.text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name="Вопрос")
    text = models.CharField(max_length=200, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")
    
    def __str__(self):
        return self.text

class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    score = models.IntegerField(verbose_name="Количество правильных ответов")
    total_questions = models.IntegerField(verbose_name="Всего вопросов")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время прохождения")

    def __str__(self):
        return f"Результат теста '{self.test.title}': {self.score}/{self.total_questions}"

    @property
    def percentage_score(self):
        if self.total_questions > 0:
            return (self.score / self.total_questions) * 100
        return 0
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Профиль пользователя с дополнительной информацией"""
    SPECIALIZATION_CHOICES = (
        ('backend', 'Backend Developer'),
        ('frontend', 'Frontend Developer'),
        ('qa', 'QA Engineer'),
        ('fullstack', 'Fullstack Developer'),
        ('devops', 'DevOps Engineer'),
    )
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name="Пользователь"
    )
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        verbose_name="Специализация"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_specialization_display()}"


class Test(models.Model):
    SPECIALIZATION_CHOICES = (
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('qa', 'QA'),
        ('fullstack', 'Fullstack'),
        ('devops', 'DevOps'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(verbose_name="Описание")
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATION_CHOICES,
        default='backend',
        verbose_name="Специализация"
    )
    time_limit_minutes = models.IntegerField(default=60, verbose_name="Лимит времени (минуты)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('single', 'Одиночный выбор'),
        ('code', 'Задача по программированию'),
    )
    
    test = models.ForeignKey(
        Test, 
        on_delete=models.CASCADE, 
        related_name='questions', 
        verbose_name="Тест"
    )
    text = models.TextField(verbose_name="Текст вопроса")
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='single',
        verbose_name="Тип вопроса"
    )
    code_template = models.TextField(
        blank=True,
        default='', 
        verbose_name="Шаблон кода",
        help_text="Начальный код для задачи по программированию"
    )
    expected_output = models.TextField(
        blank=True,
        default='', 
        verbose_name="Ожидаемый результат",
        help_text="Ожидаемый вывод программы для проверки"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['order', 'id']

    def __str__(self):
        return f"Вопрос для теста '{self.test.title}': {self.text[:50]}..."


class Answer(models.Model):
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='answers', 
        verbose_name="Вопрос"
    )
    text = models.CharField(max_length=500, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class TestResult(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Пользователь"
    )
    candidate_name = models.CharField(
        max_length=200, 
        blank=True,
        verbose_name="Имя кандидата"
    )
    score = models.IntegerField(verbose_name="Количество правильных ответов")
    total_questions = models.IntegerField(verbose_name="Всего вопросов")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время прохождения")
    time_spent_minutes = models.IntegerField(
        default=0,
        verbose_name="Затрачено времени (минуты)"
    )

    class Meta:
        verbose_name = "Результат теста"
        verbose_name_plural = "Результаты тестов"
        ordering = ['-timestamp']

    def __str__(self):
        name = self.candidate_name or (self.user.username if self.user else "Аноним")
        return f"Результат {name} по тесту '{self.test.title}': {self.score}/{self.total_questions}"

    @property
    def percentage_score(self):
        if self.total_questions > 0:
            return round((self.score / self.total_questions) * 100, 2)
        return 0


class CodeSubmission(models.Model):
    result = models.ForeignKey(
        TestResult,
        on_delete=models.CASCADE,
        related_name='code_submissions',
        verbose_name="Результат теста"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Вопрос"
    )
    code = models.TextField(verbose_name="Код")
    output = models.TextField(blank=True, verbose_name="Вывод программы")
    is_correct = models.BooleanField(default=False, verbose_name="Правильно")
    executed_at = models.DateTimeField(auto_now_add=True, verbose_name="Время выполнения")

    class Meta:
        verbose_name = "Отправленный код"
        verbose_name_plural = "Отправленный код"

    def __str__(self):
        return f"Код для вопроса {self.question.id} в результате {self.result.id}"
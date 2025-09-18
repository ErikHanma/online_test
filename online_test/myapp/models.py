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
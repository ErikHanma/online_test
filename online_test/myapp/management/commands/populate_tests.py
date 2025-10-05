from django.core.management.base import BaseCommand
# Убедитесь, что myapp.models доступна и включает 
# поля code_template и expected_output в модели Question
from myapp.models import Test, Question, Answer 


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед заполнением',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Удаление существующих данных...'))
            Test.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Данные удалены!'))

        self.stdout.write('Начинаю заполнение базы данных...\n')

        # ============================================
        # ТЕСТ 1: Backend Python Developer
        # ============================================
        self.stdout.write('Создаю Backend тест...')
        backend_test = Test.objects.create(
            title="Backend Python Developer Test",
            description="Проверка знаний Python, Django и основ backend-разработки. Тест включает вопросы по синтаксису Python, работе с данными и фреймворку Django.",
            specialization="backend",
            time_limit_minutes=30,
            is_active=True
        )

        questions_data = [
            # --------------------------------------------
            # Существующие вопросы (single)
            # --------------------------------------------
            {
                "text": "Что выведет следующий код: print(type([]))?",
                "question_type": "single",
                "answers": [
                    ("<class 'tuple'>", False),
                    ("<class 'list'>", True),
                    ("<class 'dict'>", False),
                    ("<class 'set'>", False),
                ]
            },
            {
                "text": "Какой метод используется для добавления элемента в конец списка в Python?",
                "question_type": "single",
                "answers": [
                    ("add()", False),
                    ("append()", True),
                    ("push()", False),
                    ("insert()", False),
                ]
            },
            {
                "text": "Что такое Django ORM?",
                "question_type": "single",
                "answers": [
                    ("Инструмент для работы с базами данных без SQL", True),
                    ("Система управления версиями", False),
                    ("Библиотека для работы с изображениями", False),
                    ("Фреймворк для тестирования", False),
                ]
            },
            {
                "text": "Какой HTTP метод используется для обновления существующего ресурса?",
                "question_type": "single",
                "answers": [
                    ("GET", False),
                    ("POST", False),
                    ("PUT/PATCH", True),
                    ("DELETE", False),
                ]
            },
            {
                "text": "Что делает декоратор @property в Python?",
                "question_type": "single",
                "answers": [
                    ("Создает статический метод", False),
                    ("Позволяет обращаться к методу как к атрибуту", True),
                    ("Делает метод приватным", False),
                    ("Кэширует результат метода", False),
                ]
            },
            {
                "text": "Какой код создаст словарь из двух списков keys=['a','b'] и values=[1,2]?",
                "question_type": "single",
                "answers": [
                    ("dict(keys, values)", False),
                    ("zip(keys, values)", False),
                    ("dict(zip(keys, values))", True),
                    ("{keys: values}", False),
                ]
            },
            {
                "text": "Что такое middleware в Django?",
                "question_type": "single",
                "answers": [
                    ("Компонент для обработки запросов и ответов", True),
                    ("База данных", False),
                    ("Шаблонизатор", False),
                    ("Система маршрутизации", False),
                ]
            },
            {
                "text": "Какая функция используется для создания виртуального окружения Python?",
                "question_type": "single",
                "answers": [
                    ("python -m venv", True),
                    ("pip install venv", False),
                    ("virtualenv create", False),
                    ("python env", False),
                ]
            },
            # --------------------------------------------
            # НОВЫЙ ВОПРОС ТИПА CODE (Онлайн-редактор)
            # --------------------------------------------
            {
                "text": "Напишите функцию `add_two_numbers(a, b)`, которая возвращает сумму двух чисел. Функция должна быть названа именно так.",
                "question_type": "code",
                "code_template": "def add_two_numbers(a, b):\n    # Ваш код здесь\n    pass\n\n# Пример для проверки (результат должен быть 7)\nprint(add_two_numbers(3, 4))",
                "expected_output": "7", # Ожидаемый вывод
                "answers": [],
            },
        ]

        # Цикл обработки вопросов (включая 'code')
        for i, q_data in enumerate(questions_data, 1):
            question_type = q_data.get("question_type", "single")
            
            question = Question.objects.create(
                test=backend_test,
                text=q_data["text"],
                question_type=question_type,
                # Эти поля будут заполнены только для question_type="code"
                code_template=q_data.get("code_template", ""), 
                expected_output=q_data.get("expected_output", ""),
                order=i
            )
            
            # Обрабатываем ответы только для вопросов типа 'single'
            if question_type == 'single':
                for answer_text, is_correct in q_data["answers"]:
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=is_correct
                    )

        # ============================================
        # ТЕСТ 2: Frontend Developer (Оставлен без изменений)
        # ============================================
        # ... (Код для создания Frontend теста)
        self.stdout.write('Создаю Frontend тест...')
        frontend_test = Test.objects.create(
            title="Frontend Developer Test",
            description="Оценка знаний HTML, CSS, JavaScript и современных фреймворков. Проверка понимания основ веб-разработки и создания интерактивных интерфейсов.",
            specialization="frontend",
            time_limit_minutes=25,
            is_active=True
        )

        frontend_questions = [
            {
                "text": "Какой тег используется для создания гиперссылки в HTML?",
                "question_type": "single",
                "answers": [
                    ("<link>", False),
                    ("<a>", True),
                    ("<href>", False),
                    ("<url>", False),
                ]
            },
            {
                "text": "Что означает CSS свойство 'display: flex'?",
                "question_type": "single",
                "answers": [
                    ("Скрывает элемент", False),
                    ("Включает flexbox для управления раскладкой", True),
                    ("Делает элемент прозрачным", False),
                    ("Центрирует текст", False),
                ]
            },
            {
                "text": "Какой метод добавляет элемент в конец массива в JavaScript?",
                "question_type": "single",
                "answers": [
                    ("unshift()", False),
                    ("push()", True),
                    ("append()", False),
                    ("add()", False),
                ]
            },
            {
                "text": "Что такое Virtual DOM в React?",
                "question_type": "single",
                "answers": [
                    ("Копия реального DOM в памяти для оптимизации", True),
                    ("Виртуальная машина для JavaScript", False),
                    ("Сервер для разработки", False),
                    ("База данных", False),
                ]
            },
            {
                "text": "Какое ключевое слово используется для объявления константы в JavaScript?",
                "question_type": "single",
                "answers": [
                    ("var", False),
                    ("let", False),
                    ("const", True),
                    ("constant", False),
                ]
            },
            {
                "text": "Что делает метод addEventListener()?",
                "question_type": "single",
                "answers": [
                    ("Добавляет элемент в DOM", False),
                    ("Привязывает обработчик события к элементу", True),
                    ("Создает новый элемент", False),
                    ("Удаляет элемент", False),
                ]
            },
        ]

        for i, q_data in enumerate(frontend_questions, 1):
            question_type = q_data.get("question_type", "single")
            question = Question.objects.create(
                test=frontend_test,
                text=q_data["text"],
                question_type=question_type,
                order=i
            )
            if question_type == 'single':
                for answer_text, is_correct in q_data["answers"]:
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=is_correct
                    )

        # ============================================
        # ТЕСТ 3: QA Engineer (Оставлен без изменений)
        # ============================================
        # ... (Код для создания QA теста)
        self.stdout.write('Создаю QA тест...')
        qa_test = Test.objects.create(
            title="QA Engineer Test",
            description="Проверка знаний в области тестирования ПО, автоматизации тестов и обеспечения качества. Включает вопросы по методологиям и инструментам тестирования.",
            specialization="qa",
            time_limit_minutes=20,
            is_active=True
        )

        qa_questions = [
            {
                "text": "Что такое регрессионное тестирование?",
                "question_type": "single",
                "answers": [
                    ("Тестирование новой функциональности", False),
                    ("Проверка, что изменения не сломали существующий функционал", True),
                    ("Тестирование производительности", False),
                    ("Тестирование безопасности", False),
                ]
            },
            {
                "text": "Что означает 'smoke testing'?",
                "question_type": "single",
                "answers": [
                    ("Полное тестирование всех функций", False),
                    ("Быстрая проверка основной функциональности", True),
                    ("Нагрузочное тестирование", False),
                    ("Тестирование интерфейса", False),
                ]
            },
            {
                "text": "Какой инструмент используется для автоматизации UI-тестов веб-приложений?",
                "question_type": "single",
                "answers": [
                    ("Postman", False),
                    ("Selenium", True),
                    ("JUnit", False),
                    ("Git", False),
                ]
            },
            {
                "text": "Что такое тест-кейс?",
                "question_type": "single",
                "answers": [
                    ("Набор условий для проверки функциональности", True),
                    ("Автоматизированный скрипт", False),
                    ("Баг-репорт", False),
                    ("Документация", False),
                ]
            },
            {
                "text": "Какой приоритет имеет критический баг?",
                "question_type": "single",
                "answers": [
                    ("Низкий", False),
                    ("Средний", False),
                    ("Высокий", True),
                    ("Отложенный", False),
                ]
            },
        ]

        for i, q_data in enumerate(qa_questions, 1):
            question_type = q_data.get("question_type", "single")
            question = Question.objects.create(
                test=qa_test,
                text=q_data["text"],
                question_type=question_type,
                order=i
            )
            if question_type == 'single':
                for answer_text, is_correct in q_data["answers"]:
                    Answer.objects.create(
                        question=question,
                        text=answer_text,
                        is_correct=is_correct
                    )

        # Вывод статистики
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('✅ База данных успешно заполнена!'))
        self.stdout.write('='*50)
        self.stdout.write(f'Создано тестов: {Test.objects.count()}')
        self.stdout.write(f'Создано вопросов: {Question.objects.count()}')
        self.stdout.write(f'Создано ответов: {Answer.objects.count()}')
        self.stdout.write('\n📋 Список тестов:')
        for test in Test.objects.all():
            self.stdout.write(f'  ✓ {test.title}')
            self.stdout.write(f'    - Вопросов: {test.questions.count()}')
            self.stdout.write(f'    - Время: {test.time_limit_minutes} минут')
            self.stdout.write(f'    - Специализация: {test.get_specialization_display()}')
from django.contrib import admin
from .models import Test, Question, Answer, TestResult, CodeSubmission, UserProfile


class AnswerInline(admin.TabularInline):
    """Инлайн для ответов на вопросы"""
    model = Answer
    extra = 4
    fields = ('text', 'is_correct')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка для вопросов"""
    list_display = ('text_preview', 'test', 'question_type', 'order')
    list_filter = ('test', 'question_type')
    search_fields = ('text',)
    inlines = [AnswerInline]
    list_editable = ('order',)
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Текст вопроса'


class QuestionInline(admin.TabularInline):
    """Инлайн для вопросов в тесте"""
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'order')
    show_change_link = True


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """Админка для тестов"""
    list_display = ('title', 'specialization', 'time_limit_minutes', 'questions_count', 'is_active', 'created_at')
    list_filter = ('specialization', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    inlines = [QuestionInline]
    
    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Кол-во вопросов'


class CodeSubmissionInline(admin.TabularInline):
    """Инлайн для отправленного кода"""
    model = CodeSubmission
    extra = 0
    readonly_fields = ('question', 'code', 'output', 'is_correct', 'executed_at')
    can_delete = False


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    """Админка для результатов тестов"""
    list_display = ('candidate_display', 'test', 'score', 'total_questions', 'percentage_display', 'timestamp')
    list_filter = ('test', 'timestamp')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'candidate_name')
    readonly_fields = ('test', 'user', 'candidate_name', 'score', 'total_questions', 'timestamp', 'time_spent_minutes')
    inlines = [CodeSubmissionInline]
    date_hierarchy = 'timestamp'
    
    def candidate_display(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name} ({obj.user.username})"
        return obj.candidate_name or "Аноним"
    candidate_display.short_description = 'Кандидат'
    
    def percentage_display(self, obj):
        return f"{obj.percentage_score}%"
    percentage_display.short_description = 'Процент'


@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    """Админка для отправленного кода"""
    list_display = ('result', 'question_preview', 'is_correct', 'executed_at')
    list_filter = ('is_correct', 'executed_at')
    readonly_fields = ('result', 'question', 'code', 'output', 'is_correct', 'executed_at')
    
    def question_preview(self, obj):
        return obj.question.text[:50] + '...' if len(obj.question.text) > 50 else obj.question.text
    question_preview.short_description = 'Вопрос'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Админка для профилей пользователей"""
    list_display = ('user', 'get_full_name', 'specialization', 'created_at')
    list_filter = ('specialization', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    readonly_fields = ('created_at',)
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Полное имя'
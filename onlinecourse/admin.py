from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    """Manage answer choices directly from a question in the admin."""

    model = Choice
    extra = 1


class QuestionInline(admin.StackedInline):
    """Manage mock-exam questions directly from a lesson in the admin."""

    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("content", "course", "grade")
    list_filter = ("course",)
    search_fields = ("content",)
    inlines = (ChoiceInline,)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title", "content")
    ordering = ("course", "order")
    inlines = (QuestionInline,)


admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Choice)
admin.site.register(Submission)

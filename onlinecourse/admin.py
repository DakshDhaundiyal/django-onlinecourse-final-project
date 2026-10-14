from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User

from .models import (
    Choice,
    Course,
    Lesson,
    Question,
    Submission,
    Instructor,
    Learner,
)


# Keep the Authentication and Authorization section visible in Django admin.
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)


class ChoiceInline(admin.TabularInline):
    """Edit answer choices on the question administration page."""

    model = Choice
    extra = 4


class QuestionInline(admin.StackedInline):
    """Edit questions directly on the lesson administration page."""

    model = Question
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    search_fields = ("title", "course__name")
    list_filter = ("course",)
    ordering = ("course", "order")
    inlines = (QuestionInline,)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson")
    search_fields = ("question_text",)
    list_filter = ("lesson__course",)
    inlines = (ChoiceInline,)


# Register the remaining OnlineCourse models.
admin.site.register(Course)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)
admin.site.register(Learner)

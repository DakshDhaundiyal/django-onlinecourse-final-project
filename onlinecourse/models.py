from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    content = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        related_name="questions",
        on_delete=models.CASCADE,
    )
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="choices",
        on_delete=models.CASCADE,
    )
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="submissions",
        on_delete=models.CASCADE,
    )
    student_name = models.CharField(max_length=200, default="Student")
    score = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.score}"


class SubmissionAnswer(models.Model):
    submission = models.ForeignKey(
        Submission,
        related_name="answers",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        selected = self.selected_choice or "No answer selected"
        return f"{self.question.question_text} -> {selected}"


class Instructor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Learner(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

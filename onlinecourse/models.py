from django.db import models


class Question(models.Model):
    """A mock-exam question associated with a course."""

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="questions",
    )
    content = models.CharField(max_length=1000)
    grade = models.IntegerField(default=50)

    def __str__(self):
        return f"Question: {self.content}"

    def is_get_score(self, selected_ids):
        """Return True when all correct choices are selected."""
        correct_ids = set(
            self.choices.filter(is_correct=True).values_list("id", flat=True)
        )
        selected_ids = {int(choice_id) for choice_id in selected_ids}
        return bool(correct_ids) and correct_ids == selected_ids.intersection(correct_ids)


class Choice(models.Model):
    """A selectable answer belonging to a question."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    content = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class Submission(models.Model):
    """An exam attempt linked to an enrollment and selected answers."""

    enrollment = models.ForeignKey(
        "Enrollment",
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    choices = models.ManyToManyField(
        Choice,
        related_name="submissions",
        blank=True,
    )

    def __str__(self):
        return f"Submission {self.pk} — enrollment {self.enrollment_id}"

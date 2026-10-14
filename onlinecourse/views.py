from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render

from .models import Choice, Course, Question, Submission, SubmissionAnswer


def course_details(request, course_id):
    """Display a course and its related lessons."""
    course = get_object_or_404(
        Course.objects.prefetch_related("lessons"),
        pk=course_id,
    )
    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        {"course": course},
    )


def submit(request, course_id):
    """Grade a submitted mock exam and save its answers."""
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    course = get_object_or_404(Course, pk=course_id)
    questions = list(
        Question.objects.filter(lesson__course=course)
        .select_related("lesson")
        .prefetch_related("choices")
        .order_by("lesson__order", "id")
    )

    student_name = request.POST.get("student_name", "Student").strip() or "Student"
    submission = Submission.objects.create(
        course=course,
        student_name=student_name,
        score=0,
    )

    score = 0
    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        selected_choice = None

        if selected_id:
            # Only accept a choice that belongs to the current question.
            selected_choice = next(
                (choice for choice in question.choices.all()
                 if str(choice.pk) == str(selected_id)),
                None,
            )

        is_correct = bool(selected_choice and selected_choice.is_correct)
        if is_correct:
            score += 1

        SubmissionAnswer.objects.create(
            submission=submission,
            question=question,
            selected_choice=selected_choice,
            is_correct=is_correct,
        )

    submission.score = score
    submission.save(update_fields=["score"])

    return redirect(
        "show_exam_result",
        course_id=course.pk,
        submission_id=submission.pk,
    )


def show_exam_result(request, course_id, submission_id):
    """Display the saved score and answer-by-answer exam results."""
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission.objects.prefetch_related(
            "answers__question",
            "answers__selected_choice",
        ),
        pk=submission_id,
        course=course,
    )

    answers = submission.answers.all().order_by(
        "question__lesson__order",
        "question_id",
    )
    total_questions = Question.objects.filter(lesson__course=course).count()
    percentage = (
        round((submission.score / total_questions) * 100)
        if total_questions
        else 0
    )

    results = [
        {
            "question_text": answer.question.question_text,
            "selected_choice": (
                answer.selected_choice.choice_text
                if answer.selected_choice
                else "No answer selected"
            ),
            "is_correct": answer.is_correct,
            "correct_choices": list(
                answer.question.choices.filter(is_correct=True)
                .values_list("choice_text", flat=True)
            ),
        }
        for answer in answers
    ]

    return render(
        request,
        "onlinecourse/exam_result.html",
        {
            "course": course,
            "submission": submission,
            "results": results,
            "total_questions": total_questions,
            "score": submission.score,
            "percentage": percentage,
        },
    )

from django.shortcuts import render, redirect

from src.tests.models import Question


def flashcard_view(request, pk=None):
    if not pk:
        pk = Question.objects.filter(flashcard_question__isnull=False).order_by('?').first().id
        return redirect('flash-card', pk)

    question = Question.objects.filter(id=pk).get()
    random_next = Question.objects.filter(flashcard_question__isnull=False).exclude(id=question.id).order_by('?').first().id

    return render(request, 'tests/flashcard.html', {
        'question': question,
        'random_next': random_next
    })

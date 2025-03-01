from django.shortcuts import render, redirect

from src.tests.models import Question


def index_view(request):
    return render(request, 'tests/index.html')


def random_flashcard_view(request):
    question = Question.objects.filter(flashcard_question__isnull=False).order_by('?').first()
    return redirect('flash-card', question.id)


def flashcard_view(request, pk):
    question = Question.objects.filter(id=pk).get()

    count_all = Question.objects.filter(flashcard_question__isnull=False).count()

    prev_card = Question.objects.filter(
        flashcard_question__isnull=False,
        flashcard_no__lt=question.flashcard_no
    ).order_by('flashcard_no').first()

    if not prev_card:
        prev_card = Question.objects.filter(
            flashcard_question__isnull=False
        ).order_by('flashcard_no').last()

    next_card = Question.objects.filter(
        flashcard_question__isnull=False,
        flashcard_no__gt=question.flashcard_no
    ).order_by('flashcard_no').first()

    if not next_card:
        next_card = Question.objects.filter(
            flashcard_question__isnull=False
        ).order_by('flashcard_no').first()


    return render(request, 'tests/flashcard.html', {
        'question': question,
        'prev_card': prev_card,
        'next_card': next_card,
        'count_all': count_all
    })

import uuid

from django.contrib.auth import get_user_model
from django.db import models

user_model = get_user_model()


class Question(models.Model):
    class QuestionKind(models.TextChoices):
        PZLOW_CANDIDATE = 'lc', 'PZŁ kandydat'
        PZLOW_SELECTOR = 'ls', 'PZŁ selekcjoner'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    kind = models.CharField(max_length=2, choices=QuestionKind.choices)

    question = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)
    pzlow_id = models.IntegerField(null=True)

    flashcard_no = models.IntegerField(default=0)
    flashcard_question = models.TextField(null=True)
    flashcard_answer = models.TextField(null=True)

    legal_basis = models.TextField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.question

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.flashcard_no and self.flashcard_question and self.flashcard_answer:
            _max = Question.objects.filter(flashcard_no__gt=0).order_by('-flashcard_no').first()
            if _max:
                self.flashcard_no = _max.flashcard_no + 1
            else:
                self.flashcard_no = 1

        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    pzlow_id = models.IntegerField()
    valid = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.answer


class Test(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    question_count = models.IntegerField(default=0)
    valid_answer_count = models.IntegerField(default=0)
    answered_questions_count = models.IntegerField(default=0)
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True)

    objects = models.Manager()


class TestQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.SET_NULL, null=True)
    valid = models.BooleanField(default=False)

    objects = models.Manager()
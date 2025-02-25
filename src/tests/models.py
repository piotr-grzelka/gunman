import uuid

from django.db import models


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)
    pzlow_id = models.IntegerField()

    flashcard_no = models.IntegerField(default=0)
    flashcard_question = models.TextField(null=True)
    flashcard_answer = models.TextField(null=True)

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

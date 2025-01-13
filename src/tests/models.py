import uuid

from django.db import models


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    question = models.TextField()
    image = models.CharField(max_length=255, blank=True, null=True)
    pzlow_id = models.IntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.question


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    pzlow_id = models.IntegerField()
    valid = models.BooleanField(default=False)

    objects = models.Manager()

    def __str__(self):
        return self.answer


import os

from django.core.management.base import BaseCommand
from django.db.models import Q
from openai import OpenAI

from ...models import Question, Answer


class Command(BaseCommand):
    help = 'Creates flashcards'

    def handle(self, *args, **options):
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )

        for q in Question.objects.filter(flashcard_question__isnull=False, flashcard_no=0).all():
            q.save()

        for q in Question.objects.filter(flashcard_question__isnull=True, image__isnull=True).order_by('?').all()[:1]:
            a = Answer.objects.filter(question=q, valid=True).get()

            content = "Przeformułuj następujce pytanie i odpowiedź do formatu fiszki"
            content += "\npytanie: " + q.question
            content += "\nodpowiedź: " + a.answer

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": content},
                ]
            )
            reply = response.choices[0].message.content.replace("**Pytanie:**", "").split("**Odpowiedź:**")

            print("q:", q.question)
            print("a:", a.answer)
            print("r:", reply)
            print("---------------------------------")

            q.flashcard_question = reply[0].strip()
            q.flashcard_answer = reply[1].strip()
            q.save()

import time

from django.core.management.base import BaseCommand
from django.utils.timezone import now

from ...models import Question, Answer

import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Imports questions from pzlow'

    q = 0
    currently_answered = []
    currently_answered_questions = []

    def rate(self, response):

        soup = BeautifulSoup(response.text, 'html.parser')

        for tr in soup.find_all('tr'):
            question = tr.findAll('p')
            if question:
                question = question[0].get_text()
                q = Question.objects.filter(question=question, pzlow_id__in=self.currently_answered_questions).first()
                if q:
                    print("invalid", q.id, q.question)
                else:
                    print(" - not found invalid - ", question)

        print("Question count", Question.objects.count())
        print("Valid answers", Answer.objects.filter(valid=True).count())

    def answer(self, response):
        self.q += 1

        with open('tmp/' + now().strftime('%Y-%m-%d-%H-%M-%S') + '-' + str(self.q) + '.html', 'w') as f:
            f.write(response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.find('table').find_all('tr')

        question_id = None
        question = ''
        answers = []

        img_url = None

        for tr in trs[1:]:
            # print(tr)

            if tr.find('input') == None:

                img = tr.find('img')
                if img:
                    img_url = 'https://pzlow.pl' + img['src']
                try:
                    question += tr.find('p').get_text()
                except AttributeError:
                    print(tr)
            else:
                question_id, answer_id = tr.find('input')['value'].split(';')
                answer = tr.get_text().strip().split(' ', 1)[1]

                answers.append((answer_id, answer))

        if not question_id:
            print("NO QUESTION ID")
            return

        try:
            q = Question.objects.get(pzlow_id=question_id)
        except Question.DoesNotExist:
            q = Question(pzlow_id=question_id)

        q.question = question.strip()
        q.save()

        if img_url:
            img_response = requests.get(img_url)
            img_response.raise_for_status()

            fn = f'assets/tests/q_{q.id.__str__()}.jpg'
            with open(fn, 'wb') as f:
                f.write(img_response.content)

            q.image = fn
            q.save()

        for answer_id, answer in answers:
            try:
                Answer.objects.get(pzlow_id=answer_id)
            except Answer.DoesNotExist:
                a = Answer(pzlow_id=answer_id, answer=answer, question=q)
                a.save()

        try_answer = Answer.objects.filter(question=q, valid=True).first()

        self.currently_answered_questions.append(try_answer.question.pzlow_id)

        form = soup.find('form')
        url = 'https://pzlow.pl' + form['action']

        print(url)
        response = requests.post(url, data={
            'formqst': f"{question_id};{try_answer.pzlow_id}",
            '_next': 'Dalej'
        })

        if self.q == 100:
            self.rate(response)
        else:
            self.answer(response)

    def handle(self, *args, **options):

        for i in range(0, 10):
            self.q = 0
            self.currently_answered = []
            self.currently_answered_questions = []
            response = requests.get('https://pzlow.pl/palio/html.run?_Instance=www&_PageID=251'
                                    '&_Lang=&typ=N&newser=no&_C=C_DZIALY.SZKOLENIA.SPRAWDZWIEDZE')

            soup = BeautifulSoup(response.text, 'html.parser')

            url = None
            link = soup.find_all('a')
            for l in link:
                if l.get_text() == 'Zacznij test':
                    url = l['href']

            response = requests.get('https://pzlow.pl' + url)
            self.answer(response)
            time.sleep(5)

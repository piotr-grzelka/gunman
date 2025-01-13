from django.core.management.base import BaseCommand
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, Image
from reportlab.platypus.para import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from ...models import Question, Answer

from reportlab.lib.pagesizes import A4
from PIL import Image as PilImage
pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))


class Command(BaseCommand):
    help = 'Generates PDF'

    def handle(self, *args, **options):
        doc = SimpleDocTemplate(
            "pytania.pdf", pagesize=A4,
            topMargin=20, bottomMargin=20,
            leftMargin=20, rightMargin=20
        )
        parts = []

        styles = getSampleStyleSheet()

        q_style = styles['Normal']
        q_style.fontName = 'Verdana'
        q_style.fontSize = 9
        a_style = styles['BodyText']
        a_style.fontName = 'Verdana'
        a_style.fontSize = 8

        data = []
        table_style = [
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        index = 0

        for a in Answer.objects.prefetch_related('question').filter(valid=True).order_by('question__image').all():

            image = ''
            if a.question.image:
                img = PilImage.open(a.question.image)

                width = img.width
                height = img.height

                max_height = 120

                if height > max_height:
                    ratio = max_height / height
                    width = width * ratio
                    height = height * ratio

                image = Image(a.question.image, width, height)
                table_style.append(('SPAN', (1, index), (1, index+1)))
            else:
                table_style.append(('SPAN', (0, index), (1, index)))
                table_style.append(('SPAN', (0, index+1), (1, index+1)))

            data.append([Paragraph(a.question.question, q_style), image])
            data.append([Paragraph(a.answer, a_style), ''])
            table_style.append(('LINEBELOW', (0, index+1), (-1, index+1), 0.25, colors.black))

            index +=2

        parts.append(Table(data, style=table_style, colWidths=['*', 210]), )



        doc.build(parts)

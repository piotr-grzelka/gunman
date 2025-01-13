from django.core.management.base import BaseCommand
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
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

        def add_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            text = f"{page_num}"
            canvas.setFont("Verdana", 8)
            canvas.drawRightString(200 * mm, 10 * mm, text)


        doc = SimpleDocTemplate(
            "pytania.pdf", pagesize=A4,
            topMargin=20, bottomMargin=20,
            leftMargin=20, rightMargin=20
        )
        parts = []

        q_style = ParagraphStyle(
            name='AStyleValid',
            fontName='Verdana',
            fontSize=9
        )

        a_style_valid = ParagraphStyle(
            name='AStyleValid',
            fontName='Verdana',
            fontSize=8
        )

        a_style = ParagraphStyle(
            name='AStyleValid',
            fontName='Verdana',
            fontSize=8,
            textColor=colors.gray
        )

        data = []
        table_style = [
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('CELLPADDING', (0, 0), (-1, -1), 0),
            ('CELLSPACING', (0, 0), (-1, -1), 0),
            # ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ]
        index = 0

        for question in Question.objects.order_by('image').all():

            image = ''
            if question.image:
                img = PilImage.open(question.image)

                width = img.width
                height = img.height

                max_height = 100

                if height > max_height:
                    ratio = max_height / height
                    width = width * ratio
                    height = height * ratio

                image = Image(question.image, width, height)
                table_style.append(('SPAN', (1, index), (1, index + 4)))
            else:
                table_style.append(('SPAN', (0, index), (1, index)))
                table_style.append(('SPAN', (0, index + 1), (1, index + 1)))
                table_style.append(('SPAN', (0, index + 2), (1, index + 2)))
                table_style.append(('SPAN', (0, index + 3), (1, index + 3)))
                table_style.append(('SPAN', (0, index + 4), (1, index + 4)))

            data.append([Paragraph(question.question, q_style), image])

            ak = 0
            letters = ['a)', 'b)', 'c)', 'd)']
            for answer in question.answer_set.all():
                data.append(
                    [Paragraph(letters[ak] + ' ' + answer.answer, a_style_valid if answer.valid else a_style), ''])
                ak += 1

            index += 5

        parts.append(Table(data, style=table_style, colWidths=['*', 210]) )

        doc.build(parts, add_page_number, add_page_number)

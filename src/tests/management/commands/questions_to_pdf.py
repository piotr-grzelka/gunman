from django.core.management.base import BaseCommand
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.platypus.para import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from ...models import Question, Answer

from reportlab.lib.pagesizes import A4

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
        a_style = styles['BodyText']
        a_style.fontName = 'Verdana'

        table_data = []
        table_style = [
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TEXTCOLOR', (1, 1), (-2, -2), colors.red),
        ]
        index = 0

        for q in Question.objects.all():

            table_style.append(('SPAN', (0, index), (0, index + 3)))
            aa = 0

            question = Paragraph(q.question, q_style)

            for a in Answer.objects.filter(question=q):
                table_data.append([
                    question if aa == 0 else '',
                    'X' if a.valid else '',
                    Paragraph(a.answer, a_style)
                ])
                aa += 1
                index += 1

        table = Table(data=table_data, colWidths=('*', 20, 300))
        table.setStyle(table_style)
        parts.append(table)

        doc.build(parts)

from django.core.management.base import BaseCommand

from src.barrel_finder.helpers import clean_text
from src.barrel_finder.models import Ad


class Command(BaseCommand):
    help = 'Clean description'

    def handle(self, *args, **options):
        for ad in Ad.objects.filter(clean_description__isnull=True).all():
            desc = ad.description[:500]
            ad.clean_description = clean_text(desc)
            ad.save()
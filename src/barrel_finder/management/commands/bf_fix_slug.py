from django.core.management.base import BaseCommand

from src.barrel_finder.models import Ad


class Command(BaseCommand):
    help = 'Fix slug of all ads'

    def handle(self, *args, **options):
        for ad in Ad.objects.all():
            ad.save()
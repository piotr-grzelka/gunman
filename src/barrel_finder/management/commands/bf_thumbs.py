import os

from django.conf import settings
from django.core.management.base import BaseCommand

from src.barrel_finder.helpers import resize_and_crop_image_from_url
from src.barrel_finder.models import Ad, AdImage


class Command(BaseCommand):
    def handle(self, *args, **options):
        for ad in Ad.objects.filter(thumb__isnull=True).order_by('-created_at').all()[:10]:
            image = AdImage.objects.filter(ad=ad).first()
            if not image:
                continue

            resized = resize_and_crop_image_from_url(image.url)

            if resized:
                _, extension = os.path.splitext(image.url)
                fn = '/ad/' + ad.id.__str__() + extension
                path = settings.MEDIA_ROOT + fn
                resized.save(path)
                ad.thumb = fn
                ad.save()

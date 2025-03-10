import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from src.barrel_finder.helpers import resize_and_crop_image_from_url
from src.barrel_finder.models import Ad, AdImage


class Command(BaseCommand):
    def handle(self, *args, **options):
        for ad in Ad.objects.distinct().filter(
                Q(thumb__isnull=True) | Q(thumb=''),
                thumb_failed=False,
                adimage__id__isnull=False
        ).order_by('-created_at').all()[:100]:
            print(ad.id, ad.name, end=" ")

            images = AdImage.objects.filter(ad=ad).all()

            if not images:
                continue

            for image in images:
                print("resizing")
                resized = resize_and_crop_image_from_url(image.url)

                if resized:
                    print("resized")
                    _, extension = os.path.splitext(image.url)
                    fn = '/ad/' + ad.id.__str__() + extension
                    path = settings.MEDIA_ROOT + fn
                    resized.save(path)
                    ad.thumb = fn
                    ad.save()
                    break
                else:
                    print("failed")

            if not ad.thumb:
                ad.thumb_failed = True
                ad.save()
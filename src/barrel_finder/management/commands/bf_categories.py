from django.core.management.base import BaseCommand

from src.barrel_finder.models import Category


class Command(BaseCommand):
    help = 'Get categories from portal'

    def handle(self, *args, **options):

        categories = (
            ('pistols', 'Pistolety', 0),
            ('revolvers', 'Rewolwery', 10),
            ('rifles', 'Karabiny', 20),
            ('shotguns', 'Strzelby', 30),
            ('ammo', 'Amunicja', 40),
            ('other', 'Inne', 50),
        )

        for slug, name, weight in categories:
            print("Category", slug, name, weight, end=" ")
            try:
                category = Category.objects.get(slug=slug)
                print('exists')
            except Category.DoesNotExist:
                category = Category(name=name, slug=slug, weight=weight)
                category.save()
                print('created')

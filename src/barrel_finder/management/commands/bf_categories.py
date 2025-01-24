import os

from django.core.management.base import BaseCommand
from openai import OpenAI

from src.barrel_finder.models import Category, Ad


class Command(BaseCommand):
    help = 'Get categories from portal'

    def handle(self, *args, **options):

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )

        categories = (
            ('pistols', 'Pistolety', 0, ['Pistolety']),
            ('revolvers', 'Rewolwery', 10, ['Rewolwery']),
            ('rifles', 'Karabiny', 20,
             ['Karabiny', 'broń: sztucer repetier', 'broń: kniejówka', 'broń: dryling', 'broń: sztucer łamany',
              'broń: varmint', 'broń: automat kulowy', 'broń: ekspress']),
            ('shotguns', 'Strzelby', 30,
             ['Gładkolufowa', 'broń: bock', 'broń: dubeltówka', 'broń: śrutówka powtarzalna',
              'broń: śrutówka taktyczna']),
            ('cp', 'Czarny Proch', 40, ['Broń czarnoprochowa']),
            ('ammo', 'Amunicja', 50, ['Amunicja']),
            ('other', 'Inne', 60,
             ['Optyka celownicza', 'Amunicja / elaboracja', 'Akcesoria strzeleckie', 'Części i tuning broni',
              'Pozostałe', 'Szafy, sejfy', 'Akcesoria', 'polowania', 'kolby i akcesoria', 'psy myśliwskie', 'lunety',
              'montaże', 'inne myśliwskie', 'lornetki']),
        )

        for slug, name, weight, external_categories in categories:
            print("Category", slug, name, weight, end=" ")
            try:
                category = Category.objects.get(slug=slug)
                category.weight = weight
                category.name = name
                category.save()
                print('exists')
            except Category.DoesNotExist:
                category = Category(name=name, slug=slug, weight=weight)
                category.save()
                print('created')

            for ad in Ad.objects.filter(category__isnull=True, external_category__in=external_categories).all():
                print(ad.name, ad.external_category, category, sep=" | ")
                ad.category = category
                ad.save()

        categories = "\n".join([
            n.name for n in Category.objects.all().order_by('weight')
        ])

        for ad in Ad.objects.filter(category__isnull=True).all():
            print(ad.name, ad.external_category, sep=" | ")

            content = "Znajdż kategorię dla tego ogłoszenia: " + ad.name
            content += "\n Dostępne kategorie: \n" + categories
            content += "\n\n zwróć tylko nazwę kategorii, bez innych informacji"

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": content},
                ]
            )
            reply = response.choices[0].message.content

            print("\t", reply)

            ad.category = Category.objects.get(name=reply)
            ad.save()

            break

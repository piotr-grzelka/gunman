from datetime import datetime

import pytz
from django.core.management.base import BaseCommand

from src.barrel_finder.helpers import get_portal
from src.barrel_finder.models import Ad, AdImage

from bs4 import BeautifulSoup
import requests
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        portal = get_portal('armybazar')

        for page in range(1, 5):
            time.sleep(1)
            page_url = f'http://bron-i-amunicja.armybazar.eu/pl/strona/{page}/'
            print("Page ", page, page_url)
            response = requests.get(page_url, allow_redirects=False)

            if response.status_code != 200:
                print('Error getting response from ArmyBazar', response.status_code, response.text)
                return

            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('div', {'class': 'inzerat'})[1:]
            if not items:
                print('no items')
                print(response.text)
                break
            for item in items:
                link = item.find('a')
                url = link['href']
                title = link.get_text().strip()

                price = item.find('li', {'class': 'cena'}).get_text().strip().replace('zł', '').strip()
                if price == 'Do uzgodnienia':
                    price = None

                date = item.find('li', {'class': 'datum'}).get_text().strip()
                date = datetime.strptime(date, "%d.%m.%Y%H:%M")
                date = date.replace(tzinfo=pytz.timezone('Europe/Warsaw'))

                location = item.find('li', {'class': 'lokalita'}).get_text().strip()
                badge = item.find('h2').find('span').get_text().strip()

                if badge == 'Sprzedaż':
                    kind = Ad.KIND_SELL
                elif badge == 'Zakup':
                    kind = Ad.KIND_BUY
                else:
                    continue

                print(title, url, price, kind, date, location)

                if Ad.objects.filter(external_id=url).exists():
                    continue

                time.sleep(0.2)
                response2 = requests.get(url)
                soup2 = BeautifulSoup(response2.text, 'html.parser').find('div', {'id': 'content_center'})
                description = soup2.find('p', {'class': 'popis'}).get_text().replace('Opis:', '').strip()
                title = soup2.find('h1').get_text().strip()
                t = soup2.find('h2')
                category = t.find_all('a')[-1].get_text().strip()
                external_id = t.find('strong').next_sibling.replace(':', '').strip()

                model = Ad(
                    url=url,
                    name=title,
                    price=price,
                    description=description,
                    date=date,
                    location=location,
                    kind=kind,
                    external_id=external_id,
                    external_category=category,
                    portal=portal
                )
                model.save()

                for img in soup2.find_all('a', {'class': 'fancy'}):
                    AdImage.objects.create(ad=model, url=img['href'])


from datetime import datetime

import pytz
from django.core.management.base import BaseCommand

from src.barrel_finder.helpers import get_portal
from src.barrel_finder.models import Ad

from bs4 import BeautifulSoup
import requests
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        portal = get_portal('optykamysliwska')

        for page in range(1, 3):
            print("Page ", page)
            response = requests.get(
                'https://www.optykamysliwska.pl/wyszukiwanie.html?query=7%2C0%2C0%2C%2C%2C%2C%2C%2C&page=' + str(page))

            if response.status_code != 200:
                print('Error getting response from Optykamysliwska', response.status_code, response.text)
                return

            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('table', {'class': 'Announcement'})
            for item in items:
                link = item.find('a', {'class': 'Name'})
                url = f"https://www.optykamysliwska.pl/{link['href']}"
                title = link.get_text().strip()

                if item.find('span', {'class': 'type_buy'}) is not None:
                    kind = Ad.KIND_BUY
                elif item.find('span', {'class': 'type_sell'}) is not None:
                    kind = Ad.KIND_SELL
                else:
                    continue

                print(title, url, kind)

                try:
                    Ad.objects.get(url=url)
                    continue
                except Ad.DoesNotExist:
                    ad = Ad(portal=portal)

                time.sleep(0.2)
                response2 = requests.get(url)

                if response2.status_code != 200:
                    print('Error getting response from Optykamysliwska', response2.status_code, response2.text)
                    return

                soup2 = BeautifulSoup(response2.text, 'html.parser').find('table', {'class': 'SectionTable'})

                category = soup2.find('td', {'class': 'Header'}).get_text().strip().split(':', 2)[2].strip()

                description = soup2.find('div', {'class': 'Description'}).get_text().strip()
                try:
                    price = soup2.find('span', {'class': 'Price'}).get_text().strip()
                except AttributeError:
                    price = None

                external_id = soup2.find('span', {'class': 'AnnouncementNumber'}).get_text().strip()
                date = soup2.find('span', {'class': 'PublicationDate'}).get_text().strip()
                location = soup2.find('div', {'class': 'Locality'}).get_text().replace('Lokalizacja właściciela:',
                                                                                       '').strip().split('Ogłoszenie')[
                    0].strip()

                try:
                    phone = soup2.find('div', {'class': 'ContactData'}).find('p').previous_element.get_text().replace(
                        'Bezpośredni kontakt do właściciela:', '').replace('tel:', '').strip()
                except AttributeError:
                    phone = soup2.find('div', {'class': 'ContactData'}).find('div', {
                        'class': 'Notification'}).previous_element.get_text().replace(
                        'Bezpośredni kontakt do właściciela:', '').replace('tel:', '').strip()

                # print(location, date, external_id)
                # print("phone", phone)
                # print("price", price)
                # print("--")
                # print(description)

                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                date = date.replace(tzinfo=pytz.timezone('Europe/Warsaw'))

                ad.name = title
                ad.url = url
                ad.description = description
                ad.price = price
                ad.date = date
                ad.location = location
                ad.phone = phone
                ad.external_id = external_id
                ad.kind = kind
                ad.external_category = category
                ad.save()

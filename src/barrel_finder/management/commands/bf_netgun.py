import time

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from src.barrel_finder.helpers import get_portal
from src.barrel_finder.models import Ad


class Command(BaseCommand):
    def handle(self, *args, **options):
        portal = get_portal('netgun')

        for page in range(1, 5):
            page_url = 'https://www.netgun.pl/ogloszenia?page=' + str(page)
            print("Page ", page, page_url)
            response = requests.get(page_url)

            if response.status_code != 200:
                print('Error getting response from Netgun', response.status_code, response.text)

            soup = BeautifulSoup(response.text, 'html.parser')

            items = soup.find_all('div', {'class': 'item'})
            for item in items:
                title = item.find('h3').get_text().strip()
                link = item.find('a')['href']
                price = item.find('div', {'class': 'price'}).find_all('span')[-1].get_text().strip().replace('zł',
                                                                                                             '').strip()
                description = item.find('div', {'class': 'description'}).find('p').get_text().strip()

                badge = item.find('span', {'class': 'badge'}).get_text().strip()
                if badge == 'Sprzedam':
                    kind = Ad.KIND_SELL
                elif badge == 'Kupię':
                    kind = Ad.KIND_BUY
                else:
                    continue

                print(title, link, price)

                try:
                    Ad.objects.get(url=link)
                except Ad.DoesNotExist:

                    time.sleep(.2)

                    response2 = requests.get(link)

                    if response2.status_code != 200:
                        print('Error getting response from Netgun', response.status_code, response.text)
                        continue

                    soup2 = BeautifulSoup(response2.text, 'html.parser')

                    date_div = soup2.find('div', {'class': 'date'})
                    strongs = date_div.find_all('strong')
                    external_id = strongs[0].get_text().strip()
                    date = strongs[1].get_text().strip()

                    info_divs = soup2.find('div', {'class': 'info'}).find_all('div')
                    if len(info_divs) >= 3:
                        location = info_divs[1].find('span').get_text().strip()
                        phone = info_divs[2].find('a').get_text().strip()
                    else:
                        location = None
                        phone = None

                    category = soup2.find('div', {'class': 'category'}).get_text().strip()

                    model = Ad(
                        name=title,
                        url=link,
                        price=price,
                        description=description,
                        kind=kind,
                        portal=portal,
                        external_id=external_id,
                        external_category=category,
                        date=date,
                        location=location,
                        phone=phone,

                    )

                    model.save()

            time.sleep(1)

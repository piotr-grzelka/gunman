from src.barrel_finder.models import portals, Portal

import requests
from PIL import Image
from io import BytesIO

import re


def clean_text(text):
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
        # +XX-XXX-XXX-XXXX, (XXX) XXX-XXXX, etc.
        r'\d{2,4}[-.\s]?\d{3}[-.\s]?\d{3,4}',  # XX XXX XXX, XXX-XXX-XXXX, etc.
        r'\(\d{2,4}\)\s?\d{3}[-.\s]?\d{3,4}',  # (XX) XXX-XXX
    ]

    for pattern in phone_patterns:
        text = re.sub(pattern, '### ### ###', text)

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '####@####.##', text)

    return text


def resize_and_crop_image_from_url(image_url, target_size=(300, 300)):
    try:
        # Pobierz obrazek z URL
        response = requests.get(image_url)
        response.raise_for_status()  # Sprawdź, czy nie wystąpił błąd HTTP

        # Otwórz obrazek
        image = Image.open(BytesIO(response.content))

        # Oblicz skalę, aby krótszy bok miał 300 px
        width, height = image.size
        scale = target_size[0] / min(width, height)
        new_size = (int(width * scale), int(height * scale))
        image_resized = image.resize(new_size, Image.LANCZOS)

        # Przytnij do kwadratu 300x300 px ze środka
        width, height = image_resized.size
        left = (width - target_size[0]) // 2
        top = (height - target_size[1]) // 2
        right = left + target_size[0]
        bottom = top + target_size[1]
        image_cropped = image_resized.crop((left, top, right, bottom))

        return image_cropped
    except requests.RequestException as e:
        print(f"Błąd podczas pobierania obrazu: {e}")
    except Exception as e:
        print(f"Błąd przetwarzania obrazu: {e}")


def get_portal(key):
    domain = portals[key][0]

    try:
        model = Portal.objects.get(url=domain)
    except Portal.DoesNotExist:
        model = Portal(name=portals[key][1], url=domain)
        model.save()

    return model

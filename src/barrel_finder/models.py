from django.db import models
import uuid

from django.utils.text import slugify

portals = {
    'netgun': ('https://www.netgun.pl/', 'NetGun'),
    'optykamysliwska': ('https://www.optykamysliwska.pl/', 'Optyka Myśliwska'),
    'armybazar': ('http://bron-i-amunicja.armybazar.eu/pl/', 'ArmyBazar'),
    'armoryauctions': ('https://armory-auctions.pl/', 'Armory Auctions'),
}


class Portal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Portal'
        verbose_name_plural = 'Portale'
        ordering = ['name']


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    slug = models.SlugField()
    name = models.CharField(max_length=255)
    qty = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['weight']
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'


class Ad(models.Model):
    KIND_SELL = 'sell'
    KIND_BUY = 'buy'
    KIND_CHANGE = 'change'

    KINDS = [
        (KIND_SELL, 'Sprzedaż'),
        (KIND_BUY, 'Kupno'),
        (KIND_CHANGE, 'Zamiana'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    external_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    portal = models.ForeignKey(Portal, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    url = models.URLField(null=True)
    price = models.FloatField(null=True)
    date = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    clean_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    kind = models.CharField(max_length=10, choices=KINDS, default=KIND_SELL)
    location = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    external_category = models.CharField(max_length=255, null=True)
    thumb = models.CharField(null=True)
    thumb_failed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            i = 0
            while True:
                self.slug = slugify(self.name)[:45]
                if i > 0:
                    self.slug += '-' + str(i)
                if not Ad.objects.filter(slug=self.slug).exists():
                    break

                if i > 100:
                    raise Exception('Too many slugs for name: ' + self.name)
                i += 1

        super().save(*args, force_insert=force_insert, force_update=force_update, using=using,
                     update_fields=update_fields)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Ogłoszenie'
        verbose_name_plural = 'Ogłoszenia'


class AdImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    url = models.URLField()

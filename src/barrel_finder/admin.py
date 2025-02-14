from django.contrib import admin

from src.barrel_finder.models import Portal, Category, Ad


@admin.register(Portal)
class PortalAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'qty')


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description')
    list_display = ('name', 'portal', 'category', 'kind', 'price', 'created_at', 'date')
    list_filter = ('portal', 'kind', 'category')

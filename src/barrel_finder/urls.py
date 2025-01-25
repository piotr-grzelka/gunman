from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('all', views.list_all_view, name='list-all'),
    path('all/<int:page>', views.list_all_view, name='list-all'),
    path('search', views.list_search_view, name='list-search'),
    path('c/<str:category_slug>', views.list_category_view, name='list-category'),
    path('c/<str:category_slug>/<int:page>', views.list_category_view, name='list-category'),
    path('v/<str:ad_slug>', views.ad_view, name='ad'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
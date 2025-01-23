from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('all', views.list_all_view, name='list-all'),
    path('all/<int:page>', views.list_all_view, name='list-all'),
    path('c/<str:category_slug>', views.list_category_view, name='list-category'),
    path('c/<str:category_slug>/<int:page>', views.list_category_view, name='list-category'),
    path('v/<str:ad_slug>', views.ad_view, name='ad'),
]

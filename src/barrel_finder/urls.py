from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('all', views.list_view, name='list-all'),
    path('all/<int:page>', views.list_view, name='list-all'),
    path('c/<str:category_slug>', views.list_view, name='list-all'),
    path('c/<str:category_slug>/<int:page>', views.list_view, name='list-all'),
]

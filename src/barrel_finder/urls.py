from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('all', views.list_view, name='list-all'),
    path('all/<int:page>', views.list_view, name='list-all'),
]

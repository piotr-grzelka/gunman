from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('card/random', views.random_flashcard_view, name='flash-card-random'),
    path('card/<str:pk>', views.flashcard_view, name='flash-card'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

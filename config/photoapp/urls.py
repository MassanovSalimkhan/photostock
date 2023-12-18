from django.urls import path 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'photo'


urlpatterns = [
    path('', PhotoListView.as_view(), name='list'),

    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='detail'),

    path('photo/create/', PhotoCreateView.as_view(), name='create'),

    path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name='update'),

    path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name='delete'),

   path('photo/<int:pk>/download/', PhotoDownloadView.as_view(), name='download_photo'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


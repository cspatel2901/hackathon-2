
from django.urls import path
from .views import video_feed

urlpatterns = [
    path('', video_feed, name='stream'),
    # Add other URLs as needed
]

from django.urls import path
from .views import capacity_view

urlpatterns = [
    path("", capacity_view, name="capacity"),
]

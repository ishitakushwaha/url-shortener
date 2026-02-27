from django.urls import path
from .views import CreateShortURLView, RedirectShortURLView

urlpatterns = [
    path("urls/", CreateShortURLView.as_view()),
    path("<str:short_code>/", RedirectShortURLView.as_view()),
]

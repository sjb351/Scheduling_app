from django.urls import path

from . import views  # imports views file from same folder

urlpatterns = [
    path('', views.homeView.as_view(), name="home.homeViewLink"),
    path('authrised', views.AuthorisedView.as_view()),
]
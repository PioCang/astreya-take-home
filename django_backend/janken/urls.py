""" janken URL Configuration """
from django.urls import path
from janken import views as JankenViews

urlpatterns = [
    path('register/', JankenViews.RegisterPlayer.as_view()),
    path('play_round/', JankenViews.PlayRound.as_view())
]

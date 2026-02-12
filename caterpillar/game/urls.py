# caterpillar/game/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('move/<int:game_id>/', views.make_move, name='make_move'),
    path('reset/<int:game_id>/', views.reset_game, name='reset_game'),
]
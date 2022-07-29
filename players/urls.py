from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.player_list, name='player-list'),
    path('players/new/', views.player_create, name='player-create'),
    path('players/<int:player_id>', views.player_detail, name='player-detail'),
    path('players/<int:player_id>/edit', views.player_update, name='player-update'),
    path('players/<int:player_id>/delete', views.player_delete, name='player-delete'),
    # path('players/coinrank/', views.player_coinrank, name='player-coinrank'),
]
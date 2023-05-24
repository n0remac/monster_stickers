from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:defender_id>/attack/', views.attack_view, name='attack_view'),
    path('<int:battle_id>/battle/', views.battle_view, name='battle_view'),
    path('spend_xp/<uuid:monster_id>/', views.spend_xp_view, name='spend_xp_view'),
]

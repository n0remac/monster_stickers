
from django.urls import path
from . import views

urlpatterns = [
    path('api/create_landscape/', views.create_landscape, name='create_landscape'),
    path('landscape/<uuid:pk>/', views.LandscapeDetail.as_view(), name='landscape-detail'),
    path('landscape/add_monster/', views.add_monster_to_landscape, name='add_monster_to_landscape'),
    path('landscape/take_monster/', views.take_monster_from_landscape, name='take_monster_from_landscape'),
]

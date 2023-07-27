from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.monster_list, name='monster_list'),
    # path('<str:element_type>/<str:creature>/<uuid:id>', views.monster_detail, name='monster_detail'),
    path('api/create_monster/', views.create_monster, name='create_monster'),
    path('api/get_monster/', views.get_monster_by_id, name='get_monster_by_id'),
    path('api/breed_monsters/', views.breed, name='breed_monster'),
    path('api/monsters/', views.get_monsters, name='get_monsters'),
    path('monsters/<uuid:id>', views.get_monster, name='monster_detail'),
    path('<str:element_type>/<str:creature>/claim/<uuid:monster_id>/', views.claim_monster, name='claim_monster'),
    path('monster/', include('battle.urls')),
    path('<uuid:monster_id>/breed/', views.breed_monster, name='breed_monster'),
    path('<uuid:monster1_id>/breed/<uuid:monster2_id>/', views.perform_breed, name='perform_breed'),
    path('monsters/user/', views.user_monsters, name='user_monsters')
]

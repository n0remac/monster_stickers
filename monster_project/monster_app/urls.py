from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.monster_list, name='monster_list'),
    path('<str:element_type>/<str:creature>/<uuid:id>', views.monster_detail, name='monster_detail'),
    path('api/create_monster/', views.create_monster, name='create_monster'),
    path('<str:element_type>/<str:creature>/claim/<uuid:monster_id>/', views.claim_monster, name='claim_monster'),
    path('monster/', include('battle.urls')),
]

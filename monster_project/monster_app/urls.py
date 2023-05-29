from django.urls import path, include
from . import views
from explore.views import story_list_view

urlpatterns = [
    path('', views.monster_list, name='monster_list'),
    path('<str:element_type>/<str:creature>/<uuid:id>', views.monster_detail, name='monster_detail'),
    path('api/create_monster/', views.create_monster, name='create_monster'),
    path('<str:element_type>/<str:creature>/claim/<uuid:monster_id>/', views.claim_monster, name='claim_monster'),
    path('monster/', include('battle.urls')),
    path('monster/<uuid:monster_id>/stories/', story_list_view, name='story_list_view'),
    path('<str:element_type>/<str:creature>/explore/<uuid:monster_id>', views.generate_story, name='story'),
    
]

from django.urls import path, include
from . import views

urlpatterns = [
    path('monster/<uuid:monster_id>/stories/', views.story_list_view, name='story_list_view'),
    path('story/<int:story_id>/', views.story_detail_view, name='story_detail_view'),
    path('generate/<uuid:monster_id>/', views.generate_story, name='generate_story'),
    # path('<str:element_type>/<str:creature>/story/<uuid:monster_id>', views.generate_story, name='story'),
]
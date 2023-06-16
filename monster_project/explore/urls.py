from django.urls import path, include
from . import views

urlpatterns = [
    path('monster/<uuid:monster_id>/stories/', views.story_list_view, name='story_list_view'),
    path('story/<int:story_id>/', views.story_detail_view, name='story_detail_view'),
    path('generate/<uuid:monster_id>/', views.generate_story, name='generate_story'),
    path('monsters/<uuid:monster_id>/adventures/', views.get_adventure, name='get_adventure'),
    path('monsters/move/', views.move, name='move'),
    # path('<str:element_type>/<str:creature>/story/<uuid:monster_id>', views.generate_story, name='story'),
]
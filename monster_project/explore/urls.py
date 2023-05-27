from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:element_type>/<str:creature>/story/<uuid:monster_id>', views.generate_story, name='story'),
]
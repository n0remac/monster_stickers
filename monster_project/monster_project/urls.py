from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('monster_app.urls')),
    path('', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('explore.urls')),
    path('', include('locations.urls')),
]

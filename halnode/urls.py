from django.contrib import admin
from django.urls import path, include


from frontend import urls as frontend_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('my_awesome_team.backend.urls'))
]

urlpatterns += frontend_urls.urlpatterns

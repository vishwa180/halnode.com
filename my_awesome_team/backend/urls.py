from django.urls import path
from . import views


urlpatterns = [
    path('entries/', views.EntryView.as_view()),
    path('get-projects/', views.GetProjects.as_view()),

    path('obtain-auth-token/', views.obtain_auth_token),
    path('load-user/', views.auth_load_user),
]

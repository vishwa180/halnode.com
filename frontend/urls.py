from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('careers/', views.careers, name='careers'),
    path('contact-us/', csrf_exempt(views.ContactUs.as_view()), name='contact_us'),
    path('get-started/', csrf_exempt(views.CreateLead.as_view())),
]

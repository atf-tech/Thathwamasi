from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('service', views.service, name='service'),
    path('portfolio', views.portfolio, name='portfolio'),
    path('contact', views.contact, name='contact'),
    
    # form submissions
    path('submit/index/', views.contact_message, {"page_name": "index"}, name='contact_message_index'),
    path('submit/about/', views.contact_message, {"page_name": "about"}, name='contact_message_about'),
    path('submit/contact/', views.contact_message, {"page_name": "contact"}, name='contact_message_contact'),
]
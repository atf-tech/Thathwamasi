from django.urls import path
from . import views


urlpatterns = [
    
    path('dashboard/', views.home, name='home'),
    path('dashboard/employee', views.employee, name='employee'),
    path('dashboard/login', views.login_view, name='login'),
    path('dashboard/logout', views.logout_view, name='logout'),
    path('keep-alive/', views.keep_alive, name='keep_alive'),
    path('employee_checkin', views.attendance, name='employee_checkin'),

    
]

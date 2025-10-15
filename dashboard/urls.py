from django.urls import path
from . import views


urlpatterns = [
    
    path('dashboard/', views.home, name='home'),
    path('dashboard/employee', views.employee, name='employee'),
    path('dashboard/login', views.login_view, name='login'),
    path('dashboard/logout', views.logout_view, name='logout'),
    path('employee_checkin', views.attendance, name='employee_checkin'),
    # path("get_employee/", views.get_employee_by_phone, name="get_employee_by_phone"),

    
]

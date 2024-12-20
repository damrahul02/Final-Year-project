from django.urls import path
from .views import (
    home, citizen_login, citizen_register, citizen_panel,
    citizen_profile, citizen_pass, citizen_update, logout,
    register_vaccine_part1, register_baby,
    load_districts, load_subdistricts, load_healthcare_centers,
    notification, generate_birth_certificate,volunteer_login,volunteer_panel,admin_login,
    district_dashboard

)

app_name = 'citizen'

urlpatterns = [
    path('', home, name='index'),
    path('login/', citizen_login, name='citizen_login'),
    path('register/', citizen_register, name='citizen_register'),
    path('panel/', citizen_panel, name='citizen_panel'),
    path('profile/', citizen_profile, name='citizen_profile'),
    path('pass/', citizen_pass, name='citizen_pass'),
    path('citizen_update/', citizen_update, name='citizen_update'),
    path('logout/', logout, name='logout'),
    path('register_vaccine_part1/', register_vaccine_part1, name='register_vaccine_part1'),
    path('register_baby/', register_baby, name='register_baby'),
    path('load_districts/', load_districts, name='load_districts'),
    path('load_subdistricts/', load_subdistricts, name='load_subdistricts'),
    path('load_healthcare_centers/', load_healthcare_centers, name='load_healthcare_centers'),
    path('notification/', notification, name='notification'),
    path('generate_birth_certificate/', generate_birth_certificate, name='generate_birth_certificate'),
    path('volunteer/', volunteer_login, name='volunteer_login'),
    path('volunteer/panel/', volunteer_panel, name='volunteer_panel'),
    path('admins/login/', admin_login, name='admin_login'),
    path('admins/district/', district_dashboard, name='district_dashboard'),
]

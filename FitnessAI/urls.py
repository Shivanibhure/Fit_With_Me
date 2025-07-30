"""
URL configuration for FitnessAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('login/',views.login),
    path('userlogin/',views.userlogin),
    path('dashboard/',views.dashboard,name="dashboard"),    
    path('add-profile/', views.add_profile, name='add_profile'),
    path('profile-added/',views.profile_added, name='profile_added'),
    path('modify-profile/', views.search_update, name='modify_profile'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('logout/', views.logout, name='logout'),
    
    path('generate-ai-recommendation/', views.generate_ai_recommendation, name='generate_ai_recommendation'),

    path('search-update/', views.search_update, name='search_update'),  # shows search bar + details
    path('update-profile/<str:person_name>/', views.update_profile_view, name='update_profile_view'),  # updates the data

]

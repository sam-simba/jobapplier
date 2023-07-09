from django.urls import path
from . import views

urlpatterns = [
    path('api/login/', views.loginAPI, name='api_login'),
    path('api/logout/', views.logoutAPI, name='api_logout'),

    path('', views.getRoutes),

    path('jobs/', views.getJobs),
    path('jobs/<str:pk>', views.getJob),

    path('applications/', views.getApplications),
    path('applications/<str:pk>', views.getApplication)
]

from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name='login'),
    path("logout/", views.logoutUser, name='logout'),
    path("register/", views.registerPage, name='register-page'),

    path("", views.home, name='home'),
    path("job/<str:pk>/", views.job, name='job'),
    path("post-a-job", views.postJobPage, name='post-job'),

    path("users/", views.usersPage, name='users'),
    path("user/<str:pk>/", views.userProfile, name='user-profile'),
    
    path("application/<str:pk>/", views.application, name='application'),
    path("apply/<str:pk>/", views.apply, name='apply'),

    path("delete-job/<str:pk>/", views.deleteJob, name='delete-job'),
    path("edit-job/<str:pk>/", views.editJob, name='edit-job'),
    path("delete-application/<str:pk>/", views.deleteApplication, name='delete-application'),
]
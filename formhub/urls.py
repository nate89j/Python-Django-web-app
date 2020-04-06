from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register, name='register'),
    path('profile/<profile_username>/', views.profile, name='profile'),
    path('profile/<profile_username>', views.profile, name='profile'),
    path('forgot-password', views.forgot_password, name='forgot-password'),
    path('project_add', views.project_add, name='project_add'),
    path('project_detail/<project>', views.project_detail, name='project_detail'),
    path('project_detail/<project>/', views.project_detail, name='project_detail'),
    path('project_edit/<project>', views.project_edit, name='project_edit'),
    #path('project_edit/<project>/', views.project_edit, name='project_edit'),
    path('project_edit', views.project_edit_def, name='project_edit_def'),
    path('projects', views.projects, name='projects'),
]

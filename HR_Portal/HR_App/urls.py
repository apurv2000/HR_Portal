from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
      path('',views.Admin,name='Adminpanel'),
      path('profile/', views.Profile, name='Profile'),
      path('forget_pwd/',views.Forget_pwd,name='Forget_pwd'),
      path('project/',views.Project,name='project'),
      path('project_add/',views.Project_add,name="project_add"),
      path('project_detail/',views.Project_detail,name='project_detail'),
      path('project_edit/',views.Project_edit,name='project_edit'),
      path('contact/',views.Contact,name='contact'),
      path('register/',views.Register,name='register'),
      path('register/user/', views.register_user, name='register_user'),

]

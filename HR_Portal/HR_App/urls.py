from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
      path('Adminpanel/',views.Manager,name='Adminpanel'),
      path('Hrpanel/', views.Hr, name='Hrpanel'),
      path('Emppanel/', views.Employee, name='Emppanel'),
      path('', views.Login, name='Login'),
      path('logout/', views.Logout, name='Logout'),
      path('Login/user/', views.Login_user, name='Login_user'),
      path('profile/', views.Profile, name='Profile'),
      path('forget_pwd/',views.Forget_pwd,name='Forget_pwd'),
      path('forget_password/method/',views.Forget_passord,name='Forget_password'),
      path('project/',views.Project,name='project'),
      path('project_add/',views.Project_add,name="project_add"),
      path('project_detail/',views.Project_detail,name='project_detail'),
      path('project_edit/',views.Project_edit,name='project_edit'),
      path('contact/',views.Contact,name='contact'),
      path('register/',views.Register,name='register'),
      path('register/user/', views.register_user, name='register_user'),
      path('Emplist/',views.EmpList,name='Emplist'),
      path('delete/<int:id>/', views.delete_employee, name='delete_employee'),
      path('update/<int:id>/', views.update_emp_page, name='update_employee_page'),
      path('update2/<int:id>/', views.update_employee, name='update_employee'),
      path('leave/apply/page',views.leave_Add_page,name="leaveAdd"),
      path('leave/apply/', views.Apply_leave, name="applyleave"),
      path('leave/list/',views.Leave_list,name="Leavelist"),
      path('withdraw-leave/<int:employee_id>/', views.Withdraw_leave, name='withdraw_leave'),
      path('leave/Detail/', views.leave_detail_view, name="LeaveDetail"),
      path('leave/Type/Add/', views.Leave_Type_Add, name="LeaveTypeAdd"),
      path('leave/change-status/<int:id>/<str:status>/', views.change_leave_status, name='change_leave_status'),

]

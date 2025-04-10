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
      path('withdraw-leave/<int:leave_id>/', views.Withdraw_leave, name='withdraw_leave'),
      path('leave/Detail/', views.leave_detail_view, name="LeaveDetail"),
      path('leave/Type/Add/page/', views.Leave_Type_Add, name="LeaveTypeAdd"),
      path('leave/change-status/<int:id>/<str:status>/', views.change_leave_status, name='change_leave_status'),
      path('leave/Type/Add/',views.add_leave_type,name='Addleavetype'),
      path('Handbook/', views.handdbook, name='handbook'),
      path('Learning/video/',views.Learning_Video,name='learningvideo'),
      path('Handbook/Report/', views.handbook_report, name='handbookreport'),
      path('Handbook/Employee/page', views.handbook_employee, name='handbookemployee'),
      path('Handbookupload/',views.uploadPDF,name='uploadPDF'),
      path('acknowledge-handbook/<int:pdf_id>/', views.acknowledge_handbook, name='acknowledge_handbook'),
      path('handbook-report/<int:pdf_id>/', views.handbook_Indivi_report, name='handbookempreport'),
      path('export-to-excel/', views.export_to_excel_handbook, name='export_to_excel'),
      path('leave/list/approved/', views.Leave_list_approved, name='LeavelistApproved'),
      path('leave/status/<int:leave_id>/', views.update_leave_approve, name='update_leave_status'),

]

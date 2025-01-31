from django.urls import path
from employee.views import (
    all_employees, add_employees, upload_excel, 
    view_employees, delete_employees, edit_employees, 
    export_employees_to_excel,
    manage_roles, assign_role,  user_login, logOut,
    edit_departments, add_department, delete_departments
    )

urlpatterns = [
    path('', all_employees, name='all_employees'),
    path('add_employee/', add_employees, name='add_employees'),
    path('add_department/<int:employee_id>/', add_department, name='add_department'),
    path('edit_departments/<int:department_id>/<int:employee_id>/', edit_departments, name='edit_departments'),
    path('employee/<int:employee_id>/', view_employees, name='view_employees'),
    path("employee/<int:employee_id>/edit/", edit_employees, name="edit_employees"),
    path('employee/<int:employee_id>/delete/', delete_employees, name='delete_employees'),
    path('departments/<int:employee_id>/delete/', delete_departments, name='delete_departments'),

    path('upload_excel/', upload_excel, name='upload_excel'),
    path('export/employees/', export_employees_to_excel, name='export_employees'),

    path('manage/roles/', manage_roles, name='manage_roles'),
    path('assign/role/<int:user_id>/', assign_role, name='assign_role'),

    path('user_login/', user_login, name='user_login'),
    path('logout/', logOut, name="logout"),
]
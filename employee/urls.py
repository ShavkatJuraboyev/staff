from django.urls import path
from employee.views import (
    all_employees, add_employees, upload_excel, 
    view_employees, delete_employees, edit_employees, 
    export_employees_to_excel, get_filtered_employees,
    manage_roles, assign_role,  user_login, logOut,
    )

urlpatterns = [
    path('', all_employees, name='all_employees'),
    path('add_employee/', add_employees, name='add_employees'),
    path('employee/<int:employee_id>/', view_employees, name='view_employees'),
    path("employee/<int:employee_id>/edit/", edit_employees, name="edit_employees"),
    path('employee/<int:employee_id>/delete/', delete_employees, name='delete_employees'),

    path('upload_excel/', upload_excel, name='upload_excel'),
    path('export/employees/', export_employees_to_excel, name='export_employees'),
    path('api/employees/', get_filtered_employees, name='get_filtered_employees'),

    path('manage/roles/', manage_roles, name='manage_roles'),
    path('assign/role/<int:user_id>/', assign_role, name='assign_role'),

    path('user_login/', user_login, name='user_login'),
    path('logout/', logOut, name="logout"),
]
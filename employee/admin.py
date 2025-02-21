from django.contrib import admin
from employee.models import Employee, Role, UserRole, Departments
 
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'phone', 'academic_degree', 'academic_title', 'age')
    list_filter = ('place_of_birth','academic_degree', 'academic_title', 'city')
    search_fields = ('employee_id', 'first_name', 'last_name',)


admin.site.register(Role)
admin.site.register(UserRole)
@admin.register(Departments)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('employees', 'position', 'expertise','faculty','department', 'labor_form')
    list_filter = ('department', 'labor_form', 'stavka', 'start_position')
    search_fields = ('employees__id', 'employees__first_name')
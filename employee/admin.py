from django.contrib import admin
from employee.models import Employee, Role, UserRole

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'frist_name', 'last_name', 'position')
    list_filter = ('position', 'employee_id', 'stavka', 'start_position')
    search_fields = ('employee_id', 'frist_name', 'last_name', 'position')


admin.site.register(Role)
admin.site.register(UserRole)
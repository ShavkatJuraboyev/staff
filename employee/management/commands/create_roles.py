import json
from django.core.management.base import BaseCommand
from employee.models import Role

class Command(BaseCommand):
    help = 'Rollar va ruxsatlarni yaratadi'

    def handle(self, *args, **kwargs):
        admin_permissions = {
            "add_user": True,
            "ubdate_user": True,
            "delete_user": True,
            "view_reports": True,
        }

        manager_permissions = {
            "add_user": False,
            "ubdate_user": False,
            "delete_user": False,
            "view_reports": True,
        }

        Role.objects.create(name='Admin', permissions=json.dumps(admin_permissions))
        Role.objects.create(name='Manager', permissions=json.dumps(manager_permissions))

        self.stdout.write(self.style.SUCCESS('Rollar muvaffaqiyatli yaratildi!'))

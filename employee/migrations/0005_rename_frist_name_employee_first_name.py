# Generated by Django 5.1.5 on 2025-01-29 09:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_role_options_remove_employee_contract_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='frist_name',
            new_name='first_name',
        ),
    ]

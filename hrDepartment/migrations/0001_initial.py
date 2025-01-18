# Generated by Django 5.1.4 on 2025-01-18 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id_job_title', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Должности')),
                ('job_title_name', models.CharField(max_length=255, verbose_name='Название должности')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ставка')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id_employee', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Сотрудника')),
                ('fio', models.CharField(max_length=255, verbose_name='ФИО')),
                ('passport_data', models.CharField(max_length=255, verbose_name='Паспортные данные')),
                ('date_of_birth', models.DateField(verbose_name='Дата рождения')),
                ('department', models.CharField(max_length=255, verbose_name='Отдел')),
                ('login', models.CharField(max_length=255, unique=True, verbose_name='Логин')),
                ('password', models.CharField(max_length=255, verbose_name='Пароль')),
                ('role', models.CharField(max_length=255, verbose_name='Роль')),
                ('work_phone', models.CharField(max_length=20, verbose_name='Рабочий телефон')),
                ('personal_phone', models.CharField(max_length=20, verbose_name='Личный телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('job_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrDepartment.jobtitle', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id_leave', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Отпуска')),
                ('start_date', models.DateField(verbose_name='Дата начала')),
                ('end_date', models.DateField(verbose_name='Дата окончания')),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leaves', to='hrDepartment.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Отпуск',
                'verbose_name_plural': 'Отпуска',
            },
        ),
        migrations.CreateModel(
            name='ReportOfOvertimeAndUndertime',
            fields=[
                ('id_report', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Отчета')),
                ('report_date', models.DateField(verbose_name='Дата отчета')),
                ('overtime_hours', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Часы сверхурочной работы')),
                ('undertime_hours', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Часы недоработки')),
                ('approved_by_manager', models.BooleanField(verbose_name='Одобрено менеджером')),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overtime_reports', to='hrDepartment.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Отчет о переработках и недоработках',
                'verbose_name_plural': 'Отчеты о переработках и недоработках',
            },
        ),
        migrations.CreateModel(
            name='SickLeave',
            fields=[
                ('id_sick_leave', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Больничного')),
                ('start_date_s', models.DateField(verbose_name='Дата начала')),
                ('end_date_s', models.DateField(verbose_name='Дата окончания')),
                ('supporting_documents', models.CharField(max_length=255, verbose_name='Подтверждающие документы')),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sick_leaves', to='hrDepartment.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Больничный',
                'verbose_name_plural': 'Больничные',
            },
        ),
        migrations.CreateModel(
            name='WorkTime',
            fields=[
                ('id_work_time', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Рабочего времени')),
                ('date', models.DateField(verbose_name='Дата')),
                ('time_in', models.TimeField(verbose_name='Время начала')),
                ('time_out', models.TimeField(verbose_name='Время окончания')),
                ('overtime', models.BooleanField(verbose_name='Сверхурочные')),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_time_entries', to='hrDepartment.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Рабочее время',
                'verbose_name_plural': 'Рабочее время',
            },
        ),
        migrations.CreateModel(
            name='EmployeeWorkTime',
            fields=[
                ('id_employee_work_time', models.AutoField(primary_key=True, serialize=False, verbose_name='ID Рабочего времени сотрудника')),
                ('id_employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='work_times', to='hrDepartment.employee', verbose_name='Сотрудник')),
                ('id_work_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrDepartment.worktime', verbose_name='Рабочее время')),
            ],
            options={
                'verbose_name': 'Рабочее время сотрудника',
                'verbose_name_plural': 'Рабочее время сотрудников',
            },
        ),
    ]

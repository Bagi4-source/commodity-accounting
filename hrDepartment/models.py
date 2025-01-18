from django.db import models

class Employee(models.Model):
    id_employee = models.AutoField(primary_key=True, verbose_name='ID Сотрудника')
    fio = models.CharField(max_length=255, verbose_name='ФИО')
    passport_data = models.CharField(max_length=255, verbose_name='Паспортные данные')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    job_title = models.ForeignKey('JobTitle', on_delete=models.CASCADE, verbose_name='Должность')
    department = models.CharField(max_length=255, verbose_name='Отдел')
    login = models.CharField(max_length=255, unique=True, verbose_name='Логин')
    password = models.CharField(max_length=255, verbose_name='Пароль')
    role = models.CharField(max_length=255, verbose_name='Роль')
    work_phone = models.CharField(max_length=20, verbose_name='Рабочий телефон')
    personal_phone = models.CharField(max_length=20, verbose_name='Личный телефон')
    email = models.EmailField(verbose_name='Электронная почта')

    def __str__(self):
        return f"Сотрудник: {self.fio}"

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class JobTitle(models.Model):
    id_job_title = models.AutoField(primary_key=True, verbose_name='ID Должности')
    job_title_name = models.CharField(max_length=255, verbose_name='Название должности')
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Ставка')

    def __str__(self):
        return f"Должность: {self.job_title_name}"

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

class SickLeave(models.Model):
    id_sick_leave = models.AutoField(primary_key=True, verbose_name='ID Больничного')
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sick_leaves', verbose_name='Сотрудник')
    start_date_s = models.DateField(verbose_name='Дата начала')
    end_date_s = models.DateField(verbose_name='Дата окончания')
    supporting_documents = models.CharField(max_length=255, verbose_name='Подтверждающие документы')

    def __str__(self):
        return f"Больничный №{self.id_sick_leave} для {self.id_employee}"

    class Meta:
        verbose_name = 'Больничный'
        verbose_name_plural = 'Больничные'

class Leave(models.Model):
    id_leave = models.AutoField(primary_key=True, verbose_name='ID Отпуска')
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves', verbose_name='Сотрудник')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')

    def __str__(self):
        return f"Отпуск №{self.id_leave} для {self.id_employee}"

    class Meta:
        verbose_name = 'Отпуск'
        verbose_name_plural = 'Отпуска'

class EmployeeWorkTime(models.Model):
    id_employee_work_time = models.AutoField(primary_key=True, verbose_name='ID Рабочего времени сотрудника')
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_times', verbose_name='Сотрудник')
    id_work_time = models.ForeignKey('WorkTime', on_delete=models.CASCADE, verbose_name='Рабочее время')

    def __str__(self):
        return f"Рабочее время №{self.id_work_time} для {self.id_employee}"

    class Meta:
        verbose_name = 'Рабочее время сотрудника'
        verbose_name_plural = 'Рабочее время сотрудников'

class WorkTime(models.Model):
    id_work_time = models.AutoField(primary_key=True, verbose_name='ID Рабочего времени')
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_time_entries', verbose_name='Сотрудник')
    date = models.DateField(verbose_name='Дата')
    time_in = models.TimeField(verbose_name='Время начала')
    time_out = models.TimeField(verbose_name='Время окончания')
    overtime = models.BooleanField(verbose_name='Сверхурочные')

    def __str__(self):
        return f"Рабочее время №{self.id_work_time} для {self.id_employee} на {self.date}"

    class Meta:
        verbose_name = 'Рабочее время'
        verbose_name_plural = 'Рабочее время'

class ReportOfOvertimeAndUndertime(models.Model):
    id_report = models.AutoField(primary_key=True, verbose_name='ID Отчета')
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='overtime_reports', verbose_name='Сотрудник')
    report_date = models.DateField(verbose_name='Дата отчета')
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Часы сверхурочной работы')
    undertime_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Часы недоработки')
    approved_by_manager = models.BooleanField(verbose_name='Одобрено менеджером')

    def __str__(self):
        return f"Отчет №{self.id_report} для {self.id_employee} на {self.report_date}"

    class Meta:
        verbose_name = 'Отчет о переработках и недоработках'
        verbose_name_plural = 'Отчеты о переработках и недоработках'
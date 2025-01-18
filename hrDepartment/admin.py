from django.contrib import admin
from .models import Employee, JobTitle, SickLeave, Leave, EmployeeWorkTime, WorkTime, ReportOfOvertimeAndUndertime

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('fio', 'job_title', 'department', 'email', 'work_phone', 'personal_phone')
    search_fields = ('fio', 'department', 'email', 'work_phone', 'personal_phone')
    list_filter = ('department', 'job_title')

@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ('job_title_name', 'rate')
    search_fields = ('job_title_name',)
    list_filter = ('rate',)

@admin.register(SickLeave)
class SickLeaveAdmin(admin.ModelAdmin):
    list_display = ('id_sick_leave', 'id_employee', 'start_date_s', 'end_date_s', 'supporting_documents')
    search_fields = ('id_employee__fio', 'supporting_documents')
    list_filter = ('start_date_s', 'end_date_s')

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id_leave', 'id_employee', 'start_date', 'end_date')
    search_fields = ('id_employee__fio',)
    list_filter = ('start_date', 'end_date')

@admin.register(EmployeeWorkTime)
class EmployeeWorkTimeAdmin(admin.ModelAdmin):
    list_display = ('id_employee_work_time', 'id_employee', 'id_work_time')
    search_fields = ('id_employee__fio',)

@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ('id_work_time', 'id_employee', 'date', 'time_in', 'time_out', 'overtime')
    search_fields = ('id_employee__fio', 'date')
    list_filter = ('date', 'overtime')

@admin.register(ReportOfOvertimeAndUndertime)
class ReportOfOvertimeAndUndertimeAdmin(admin.ModelAdmin):
    list_display = ('id_report', 'id_employee', 'report_date', 'overtime_hours', 'undertime_hours', 'approved_by_manager')
    search_fields = ('id_employee__fio', 'report_date')
    list_filter = ('report_date', 'approved_by_manager')

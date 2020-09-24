from django.contrib import admin

from schedules.models import Specialty
from schedules.models import Doctor
from schedules.models import Schedule
from schedules.models import AvailableTimes
from schedules.models import Appointment


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ['name']



@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name']
    filter_horizontal = ['specialties']


class AvailableTimesStackedInline(admin.StackedInline):
    model = AvailableTimes
    extra = 0


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'day', 'created_at']
    inlines = [AvailableTimesStackedInline]


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'schedule', 'hour', 'created_at']
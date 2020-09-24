from rest_framework import routers

from schedules.api import SpecialtyViewSet
from schedules.api import DoctorViewSet
from schedules.api import ScheduleViewSet
from schedules.api import AppointmentViewSet
from core.api import AuthViewSet



router = routers.DefaultRouter(trailing_slash=True)
router.register(r'specialties', SpecialtyViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'schedule', ScheduleViewSet)
router.register(r'appointment', AppointmentViewSet)
router.register(r'auth', AuthViewSet)

import json
import datetime
from rest_framework import serializers

from core.models import Account

from schedules.models import Specialty
from schedules.models import Doctor
from schedules.models import Schedule
from schedules.models import AvailableTimes
from schedules.models import Appointment


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = ['id', 'name']


class DoctorSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = Doctor
        depth = 1
        fields = '__all__'


class AvailableTimesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AvailableTimes
        fields = ['hour']


class ScheduleSerializer(serializers.ModelSerializer):
    hours = serializers.SerializerMethodField()
        
    class Meta:
        model = Schedule
        depth = 2
        fields = ['id', 'doctor', 'day', 'hours']
                
    def get_hours(self, obj):
        return AvailableTimesSerializer(AvailableTimes.objects.filter(schedule=obj, hour__gte=datetime.datetime.now().time()), many=True).data



class AppointmentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Appointment
        fields = ['user', 'schedule', 'hour']
    
    
    # def save(self, **kwargs):
    #     request = self.context.get('request', None)
        
    #     if request:
    #         kwargs = request.data
    #         kwargs['user'] = Account.objects.get(id=request.user.id)
    #     return super(AppointmentSerializer, self).save(**kwargs)


class AppointmentSerializerRead(serializers.ModelSerializer):
        
    class Meta:
        model = Appointment
        depth = 3
        fields = ['schedule', 'hour']
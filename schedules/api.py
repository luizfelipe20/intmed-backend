from django.utils import timezone
import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from core.models import Account

from schedules.models import Specialty
from schedules.models import Doctor
from schedules.models import Schedule
from schedules.models import Appointment
from schedules.models import AvailableTimes

from schedules.serializers import DoctorSerializer
from schedules.serializers import SpecialtySerializer
from schedules.serializers import ScheduleSerializer
from schedules.serializers import AppointmentSerializer
from schedules.serializers import AppointmentSerializerRead


class SpecialtyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]
    
    @action(detail=False, methods=['post'])
    def save_image(self, request, *args, **kwargs):
        from music_platform.serializers import ImageSerializer

        _data = request.data

        if LastUserAssistedLive.objects.filter(user=request.user).exists():
            live = LastUserAssistedLive.objects.get(user=request.user).live
            _data["live"] = live.id

        if not "_image" in _data:
            return Response("É necessário informar a imagem.", status=status.HTTP_400_BAD_REQUEST)

        if len(_data["_image"]) == 0:
            return Response("Base64 inválido.", status=status.HTTP_400_BAD_REQUEST)

        serializer = ImageSerializer(data=_data)
        serializer.is_valid()
        serializer.save()

        return Response("Registrado com sucesso.", status=status.HTTP_201_CREATED)

        
class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filter_fields = ['specialties']



class ScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Schedule.objects.order_by('day')
    serializer_class = ScheduleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['doctor__name']
    filter_fields = ['doctor__specialties']

    def list(self, request, *args, **kwargs):
        day_now = datetime.date.today()
        self.queryset = self.queryset.filter(day__gte=datetime.date(day_now.year, day_now.month, day_now.day))
        return super(ScheduleViewSet, self).list(request, *args, **kwargs)



class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.order_by('schedule__day')
    serializer_class = AppointmentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['schedule__doctor__name']
    filter_fields = ['schedule__doctor__specialties']
    day_now = datetime.date.today()
    
    def list(self, request, *args, **kwargs):    
        self.serializer_class = AppointmentSerializerRead
        self.queryset = self.queryset.filter(user=request.user, schedule__day__gte=datetime.date(self.day_now.year, self.day_now.month, self.day_now.day), hour__gte=datetime.datetime.now().time())
        return super(AppointmentViewSet, self).list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        return serializer.save(user=Account.objects.get(id=self.request.user.id))
    
    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        time_str = "{}:00".format(data["hour"])
        time_object = datetime.datetime.strptime(time_str, "%H:%M:%S").time()
                
        if not Schedule.objects.filter(id=data["schedule"]).exists():
            return Response("Agendamento não encontrado.", status=status.HTTP_400_BAD_REQUEST)
        else:
            if not AvailableTimes.objects.filter(schedule__id=data["schedule"], hour=time_object).exists():
                return Response("Horário para consulta não disponível.", status=status.HTTP_400_BAD_REQUEST)

            if AvailableTimes.objects.filter(
                schedule__id=data["schedule"], 
                hour=time_object, 
                schedule__day__lte=datetime.date(self.day_now.year, self.day_now.month, self.day_now.day), 
                hour__lte=datetime.datetime.now().time()).exists():
                return Response("Consultas não podem ser marcadas, com datas passadas.", status=status.HTTP_400_BAD_REQUEST)

        if self.queryset.filter(**data, user=request.user).exists():
            return Response("Este usuário ja fez o resgitro desta consulta.", status=status.HTTP_400_BAD_REQUEST)    
        
        if not self.queryset.filter(**data).exists():
            return Response("Dia e horário não disponível para consulta.", status=status.HTTP_400_BAD_REQUEST)

        instance = self.perform_create(serializer)
        serializer = AppointmentSerializerRead(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, pk, *args, **kwargs):  
        if not self.queryset.filter(pk=pk).exists():
            return Response("Consulta não encontrada.", status=status.HTTP_400_BAD_REQUEST)
        
        if not self.queryset.filter(pk=pk, user=request.user).exists():
            return Response("Este usuário não realizou o agendamento desta consulta.", status=status.HTTP_400_BAD_REQUEST)    
        
        if self.queryset.filter(
            pk=pk,
            schedule__day__lte=datetime.date(self.day_now.year, self.day_now.month, self.day_now.day), 
            hour__lte=datetime.datetime.now().time()
            ).exists():
            return Response("Esta consulta já foi realizada.", status=status.HTTP_400_BAD_REQUEST)
        
        return super(AppointmentViewSet, self).destroy(request, *args, **kwargs)
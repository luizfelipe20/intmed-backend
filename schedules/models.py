from django.db import models
from rest_framework.exceptions import ValidationError

from core.variables_constants import STATUS
from core.models import Account


class Specialty(models.Model):
    name = models.CharField(verbose_name="especialidade", max_length=255, blank=False, null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="criado em")
    
    class Meta:
        verbose_name = "Especialidade"
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(verbose_name="nome", max_length=255, blank=False, null=True)
    crm = models.CharField(max_length=255, blank=False, null=True)
    email = models.CharField(verbose_name="email", max_length=255, blank=False, null=True)
    phone = models.CharField(verbose_name="telefone", max_length=255, blank=False, null=True)
    specialties = models.ManyToManyField(Specialty, verbose_name="especialidades", blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="criado em")
    
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

    def __str__(self):
        return self.name


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=False, verbose_name="médico")
    day = models.DateField(null=True, blank=False, verbose_name="dia", error_messages={'unique_together': ''})
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="criado em")
    
    class Meta:
        unique_together = ['doctor', 'day']
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
    
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('doctor', 'day'):
            return 'Este data já foi registrada para este médico.'
        else:
            return super(Schedule, self).unique_error_message(model_class, unique_check)

    def __str__(self):
        return "{} - {}".format(self.doctor, self.day)
    

class AvailableTimes(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=False)
    hour = models.TimeField(null=False, blank=True, verbose_name="horário")
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="criado em")
    
    class Meta:
        unique_together = ['schedule', 'hour']
        verbose_name = "Horário"
        verbose_name_plural = "Horários"
    
    def unique_error_message(self, model_class, unique_check):
        if model_class == type(self) and unique_check == ('schedule', 'hour'):
            return 'Este horário já foi registrado para esta data.'
        else:
            return super(AvailableTimes, self).unique_error_message(model_class, unique_check)


class Appointment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=False, verbose_name="usuário")
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=False, verbose_name="agenda")
    hour = models.TimeField(null=False, blank=True, verbose_name="horário")
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="criado em")

    
    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"
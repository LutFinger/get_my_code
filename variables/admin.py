from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.DevicesModel)
class DevicesModel(admin.ModelAdmin):
    list_display = ['devices_name',
                    'devices_ip',
                    'connection_protocol',
                    'communication_type',
                    'communication_port']

@admin.register(models.VariableModel)
class VariableModel(admin.ModelAdmin):
    list_display = ['device_id',
                    'variable_name',
                    'variable_address',
                    'variable_type',
                    'variable_value']

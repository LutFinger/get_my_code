from django.contrib import admin
from . import models


@admin.register(models.CurrentCommunicationModel)
class CurrentCommunicationModelAdmin(admin.ModelAdmin):
    list_display = ['variable_id',
                    'receive_or_transmit',
                    'periodically_or_request',
                    'transmit_value',
                    'received_value',
                    'order_request',
                    'communication_status',
                    'variable_value_status']

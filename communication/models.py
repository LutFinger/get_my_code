from django.db import models
from main.models import DateTimeStampedModel
from variables.models import VariableModel


class CurrentCommunicationModel(DateTimeStampedModel):
    RECEIVE_OR_TRANSMIT = [(False, 'received'),
                           (True, 'transmit')]

    PERIODICALLY_OR_REQUEST = [(False, 'on request'),
                               (True, 'periodically')]

    COMMUNICATION_STATUS = [(0, 'none'),
              (1, 'received'),
              (2, 'transmitted'),
              (3, 'updated'),
              (4, 'communication error'),
              (5, 'receive error'),
              (6, 'transmit error')]

    CHANGING_VARIABLE_VALUE = [(False, 'value changed'),
                               (True, 'value not changed')]

    ORDER_REQUEST = [(True, 'in progress'),
                     (False, 'done')]

    variable_id = models.ForeignKey(VariableModel, on_delete=models.CASCADE, null=True, blank=True)
    transmit_value = models.PositiveIntegerField(blank=True, null=True)
    received_value = models.PositiveIntegerField(blank=True, null=True)
    receive_or_transmit = models.BooleanField(choices=RECEIVE_OR_TRANSMIT, default=False)
    periodically_or_request = models.BooleanField(choices=PERIODICALLY_OR_REQUEST, default=False)
    order_request = models.BooleanField(choices=ORDER_REQUEST, default=True)
    communication_status = models.PositiveSmallIntegerField(choices=COMMUNICATION_STATUS, default=0)
    changing_variable_value = models.BooleanField(choices=CHANGING_VARIABLE_VALUE, null=True, blank=True)

    class Meta:
        unique_together = ['variable_id', 'receive_or_transmit', 'periodically_or_request']
        verbose_name = 'Current communication'
        verbose_name_plural = 'Current communications'

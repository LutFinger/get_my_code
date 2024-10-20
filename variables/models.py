from django.db import models
from main.models import DateTimeStampedModel


class DevicesModel(DateTimeStampedModel):
    PROTOCOL = [
        (0, 'modbus_tcp'),
        (1, 'tcp_ip'),
        (2, 'MELSEC Q'),
        (3, 'MELSEC iQ-R')
    ]

    TYPE = [
        (0, 'binary'),
        (1, 'ascii'),
    ]

    devices_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    devices_ip = models.CharField(max_length=15, blank=True, null=True)
    connection_protocol = models.PositiveIntegerField(choices=PROTOCOL, default=0)
    communication_type = models.PositiveIntegerField(choices=TYPE, blank=True, null=True)
    communication_port = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        ordering = ('devices_name',)
        unique_together = ('devices_name', 'devices_ip', 'connection_protocol', 'communication_type', 'communication_port')
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'

    def __str__(self):
        return str(self.devices_name + ' ' + self.devices_ip)


class VariableModel(DateTimeStampedModel):
    TYPE_VARIABLE = [
        (0, 'boolean'),
        (1, 'integer'),
        (2, 'float'),
        (3, 'string'),
    ]

    device_id = models.ForeignKey(DevicesModel, on_delete=models.CASCADE, blank=False, null=True)
    variable_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    variable_address = models.CharField(max_length=100, blank=False, null=False)
    variable_type = models.PositiveIntegerField(choices=TYPE_VARIABLE, default=0)
    variable_value = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ('variable_address',)
        unique_together = ('device_id', 'variable_name', 'variable_address')
        verbose_name = 'Variable'
        verbose_name_plural = 'Variables'

    def __str__(self):
        return str(self.variable_name + ' ' + self.variable_address)

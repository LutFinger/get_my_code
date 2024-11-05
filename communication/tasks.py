import django

django.setup()
from celery import shared_task
from celery.utils.log import get_task_logger
from variables.models import DevicesModel, VariablesModel
from pymodbus.client import ModbusTcpClient
from communication.models import CurrentCommunicationModel
import time

logger = get_task_logger(__name__)


@shared_task()
def modbus_communication():
    print('communication_start')

    all_current_communications = CurrentCommunicationModel.objects.all()
    all_devices = DevicesModel.objects.filter(connection_protocol=0)

    variables_for_current_receive_id_list = []
    variables_for_current_transmit_id_list = []

    receive_ip_list = []
    receive_port_list = []
    receive_address_list = []
    receive_type_list = []

    transmit_ip_list = []
    transmit_port_list = []
    transmit_address_list = []
    transmit_type_list = []
    transmit_value_list = []

    for device in all_devices:

        for current_communication in all_current_communications:
            variable = VariablesModel.objects.filter(id=current_communication.variable_id.id)

            if device.id == variable[0].device_id:

                if current_communication.order_request:

                    if current_communication.periodically_or_request:

                        if current_communication.receive_or_transmit is False:
                            variables_for_current_receive_id_list.append(current_communication.id)
                            receive_ip_list.append(device.devices_ip)
                            receive_port_list.append(device.communication_port)
                            receive_address_list.append(variable[0].variable_address)
                            receive_type_list.append(variable[0].variable_type)

                        if (current_communication.receive_or_transmit and
                                current_communication.transmit_value != current_communication.received_value):
                            variables_for_current_transmit_id_list.append(current_communication.id)
                            transmit_ip_list.append(device.devices_ip)
                            transmit_port_list.append(device.communication_port)
                            transmit_address_list.append(variable[0].variable_address)
                            transmit_type_list.append(variable[0].variable_type)
                            transmit_value_list.append(current_communication.transmit_value)

                    elif current_communication.periodically_or_request is False:

                        if current_communication.receive_or_transmit is False:
                            variables_for_current_receive_id_list.append(current_communication.id)
                            receive_ip_list.append(device.devices_ip)
                            receive_port_list.append(device.comunication_port)
                            receive_address_list.append(variable[0].variable_address)
                            receive_type_list.append(variable[0].variable_type)

                        if (current_communication.receive_or_transmit and
                                current_communication.order_request is True):
                            variables_for_current_transmit_id_list.append(current_communication.id)
                            transmit_ip_list.append(device.devices_ip)
                            transmit_port_list.append(device.comunication_port)
                            transmit_address_list.append(variable[0].variable_address)
                            transmit_type_list.append(variable[0].variable_type)
                            transmit_value_list.append(current_communication.transmit_value)

    if variables_for_current_receive_id_list:
        variables_for_current_receive_dictionary = {'id': variables_for_current_receive_id_list,
                                                     'ip': receive_ip_list,
                                                     'port': receive_port_list,
                                                     'address': receive_address_list,
                                                     'type': receive_type_list}
    else:
        variables_for_current_receive_dictionary = {}

    if variables_for_current_transmit_id_list:
        variables_for_current_transmit_dictionary = {'id': variables_for_current_transmit_id_list,
                                                     'ip': transmit_ip_list,
                                                     'port': transmit_port_list,
                                                     'address': transmit_address_list,
                                                     'type': transmit_type_list,
                                                     'value': transmit_value_list}
    else:
        variables_for_current_transmit_dictionary = {}

    if variables_for_current_transmit_dictionary:
        index = 0
        id_list = variables_for_current_transmit_dictionary['id']
        max_index = len(id_list)
        change_ip = True
        list_end = False
        condition_client = ModbusTcpClient

        for current_transmit_id in id_list:
            non_connection = False

            get_current_transmit = CurrentCommunicationModel.objects.get(id=current_transmit_id)
            get_current_variable = VariablesModel.objects.get(id=get_current_transmit.variable_id.id)

            ip = variables_for_current_transmit_dictionary['ip'][index]
            port = variables_for_current_transmit_dictionary['port'][index]
            address = variables_for_current_transmit_dictionary['address'][index]
            type = variables_for_current_transmit_dictionary['type'][index]
            value = variables_for_current_transmit_dictionary['value'][index]

            if change_ip or index == 0:
                condition_client = ModbusTcpClient(host=ip, port=port)

                try:
                    condition_client.connect()

                except:
                    non_connection = True
                    get_current_transmit.communication_status = 4
                    get_current_transmit.save()
                    get_current_variable.save()

            if non_connection is False:

                if str(type) == 'integer':

                    try:
                        condition_client.write_register(
                            address=int(address), value=int(value))

                        time.sleep(1)

                        received_value = condition_client.read_holding_registers(
                            address=int(address), count=1)

                        if int(get_current_transmit.transmit_value) != int(received_value.registers[0]):
                            get_current_transmit.variable_value_status = True

                        elif int(get_current_transmit.transmit_value) == int(received_value.registers[0]):
                            get_current_transmit.variable_value_status = False

                        get_current_transmit.received_value = int(received_value.registers[0])
                        get_current_variable.variable_value = int(received_value.registers[0])

                        if received_value.registers[0] == value:

                            if get_current_transmit.communication_status == 0:
                                get_current_transmit.communication_status = 2

                            else:
                                get_current_transmit.communication_status = 3

                            if get_current_transmit.periodically_or_request == False:
                                get_current_transmit.order_request = False

                        elif received_value.registers[0] != value:
                            get_current_transmit.communication_status = 6

                    except:
                        get_current_transmit.communication_status = 6
                        get_current_transmit.save()
                        get_current_variable.save()

                elif str(type) == 'boolean':

                    try:
                        condition_client.write_coil(
                            address=int(address), value=bool(value))

                        time.sleep(1)

                        received_value = condition_client.read_coils(
                            address=int(address), count=1)

                        if int(get_current_transmit.transmit_value) != int(received_value.bits[0]):
                            get_current_transmit.variable_value_status = True

                        elif int(get_current_transmit.transmit_value) == int(received_value.bits[0]):
                            get_current_transmit.variable_value_status = False

                        get_current_transmit.received_value = int(received_value.bits[0])
                        get_current_variable.variable_value = int(received_value.bits[0])

                        if received_value.bits[0] == value:

                            if get_current_transmit.communication_status == 0:
                                get_current_transmit.communication_status = 2

                            else:
                                get_current_transmit.communication_status = 3

                            if get_current_transmit.periodically_or_request == False:
                                get_current_transmit.order_request = False

                        elif received_value.bits[0] != value:
                            get_current_transmit.communication_status = 6

                    except:
                        get_current_transmit.communication_status = 6
                        get_current_transmit.save()
                        get_current_variable.save()

            get_current_transmit.save()
            get_current_variable.save()

            next_index = index + 1

            if next_index < max_index:
                next_ip = variables_for_current_transmit_dictionary['ip'][next_index]

                if next_ip != ip:
                    change_ip = True

                elif next_ip == ip:
                    change_ip = False

            elif next_index == max_index:
                list_end = True

            if change_ip or list_end:
                condition_client.close()
                time.sleep(1)

            index = index + 1

    if variables_for_current_receive_dictionary:
        index = 0
        id_list = variables_for_current_receive_dictionary['id']
        max_index = len(id_list)
        change_ip = True
        list_end = False
        condition_client = None

        for current_receive_id in id_list:
            non_connection = False
            get_current_received = CurrentCommunicationModel.objects.get(id=current_receive_id)
            get_current_variable = VariablesModel.objects.get(id=get_current_received.variable_id.id)
            ip = variables_for_current_receive_dictionary['ip'][index]
            port = variables_for_current_receive_dictionary['port'][index]
            address = variables_for_current_receive_dictionary['address'][index]
            type = variables_for_current_receive_dictionary['type'][index]

            if change_ip or index == 0:
                condition_client = ModbusTcpClient(host=ip, port=port)

                try:
                    condition_client.connect()

                except:
                    non_connection = True
                    get_current_received.communication_status = 4
                    get_current_received.save()

            if non_connection is False:

                if str(type) == 'integer':

                    try:
                        received_value = condition_client.read_holding_registers(
                            address=int(address), count=1)

                        if get_current_received.received_value != None:

                            if int(get_current_received.received_value) != int(received_value.registers[0]):
                                get_current_received.variable_value_status = True

                            elif int(get_current_received.received_value) == int(received_value.registers[0]):
                                get_current_received.variable_value_status = False

                        get_current_received.received_value = int(received_value.registers[0])
                        get_current_variable.variable_value = int(received_value.registers[0])

                        if get_current_received.periodically_or_request == False:
                            get_current_received.order_request = False

                        if get_current_received.communication_status == 0:
                            get_current_received.communication_status = 1

                        else:
                            get_current_received.communication_status = 3

                    except:
                        get_current_received.communication_status = 5
                        get_current_received.save()
                        get_current_variable.save()

                elif str(type) == 'boolean':

                    try:
                        received_value = condition_client.read_coils(
                            address=int(address), count=1)

                        if get_current_received.received_value != None:

                            if int(get_current_received.received_value) != int(received_value.bits[0]):
                                get_current_received.variable_value_status = True

                            elif int(get_current_received.received_value) == int(received_value.bits[0]):
                                get_current_received.variable_value_status = False

                        get_current_received.received_value = int(received_value.bits[0])
                        get_current_variable.variable_value = str(received_value.bits[0])

                        if get_current_received.periodically_or_request == False:
                            get_current_received.order_request = False

                        if get_current_received.communication_status == 0:
                            get_current_received.communication_status = 1

                        else:
                            get_current_received.communication_status = 3

                    except:
                        get_current_received.communication_status = 5
                        get_current_received.save()
                        get_current_variable.save()

            get_current_received.save()
            get_current_variable.save()

            next_index = index + 1

            if next_index < max_index:
                next_ip = variables_for_current_receive_dictionary['ip'][next_index]

                if next_ip != ip:
                    change_ip = True

                elif next_ip == ip:
                    change_ip = False

            elif next_index == max_index:
                list_end = True

            if change_ip or list_end:
                condition_client.close()
                time.sleep(1)

            index = index + 1

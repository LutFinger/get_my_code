# ----------------------------------------------------------------------------------------------------------------------
# import
from django import forms
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Row, Fieldset, Div, HTML, Button
from . import models


# /////////////////////////////////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#                                                 Devices & variables
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\/////////////////////////////////////////////////////////////

# ----------------------------------------------------------------------------------------------------------------------
# Create

class DevicesCreateForm(forms.ModelForm):
    class Meta:
        model = models.DevicesModel
        fields = ['devices_name',
                  'devices_ip',
                  'connection_protocol',
                  'communication_type',
                  'communication_port']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['devices_name'].label = 'Nazwa'
        self.fields['connection_protocol'].label = 'Protokół'
        self.fields['devices_ip'].label = 'Adres ip'
        self.fields['communication_port'].label = 'Port'
        self.fields['communication_type'].label = 'Typ danych'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'devices-create-form'
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('devices_name', css_class="form-control", title="Wpisz nawę urządzenia"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
                Div(
                    Field('devices_ip', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
                Div(
                    Field('communication_port', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
                Div(
                    Field('communication_type', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
                Div(
                    Field('connection_protocol', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
            ),
            Row(
                Div(
                    FormActions(
                        Submit('submit', 'Zapisz', css_class='btn btn-success'),
                        Button('cancel', 'Anuluj', css_class='btn btn-dark-primary', onclick='history.go(-1);')
                    ), css_class="col-6 text-center", style="margin: auto"
                )
            )
        )

    pass


class VariablesCreateForm(forms.ModelForm):
    class Meta:
        model = models.VariablesModel
        fields = ['variable_name',
                  'variable_address',
                  'variable_type',
                  'variable_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['variable_name'].label = 'Nazwa zmiennej'
        self.fields['variable_address'].label = 'Adres zmiennej'
        self.fields['variable_type'].label = 'Typ zmiennej'
        self.fields['variable_value'].label = 'Wartość zmiennej'
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'variables-create-form'
        self.helper.layout = Layout(
            Row(
                Div(
                    Field('variable_name', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
                Div(
                    Field('variable_address', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
                Div(
                    Field('variable_type', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
                Div(
                    Field('variable_value', css_class="form-control", title="Wpisz nawę recepty"),
                    css_class="col-7 text-left", style="margin: auto"
                ),
            ),
            Row(
                Div(
                    FormActions(
                        Submit('submit', 'Zapisz', css_class='btn btn-success'),
                        Button('cancel', 'Anuluj', css_class='btn btn-dark-primary', onclick='history.go(-1);')
                    ), css_class="col-6 text-center", style="margin: auto"
                )
            )
        )

    pass

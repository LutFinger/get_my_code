from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView, TemplateView
from . import models, forms


class DevicesAndVariablesView(TemplateView):
    template_name = 'variables/list.html'

    def get_context_data(self, **kwargs):
        devices_create_form = forms.DevicesCreateForm()
        variables_create_form = forms.VariablesCreateForm()
        devices_variables_list = models.DevicesModel.objects.all()
        variables_list = models.VariablesModel.objects.all()
        context = super(DevicesAndVariablesView, self).get_context_data(**kwargs)
        context.update({
            'devices_create_form': devices_create_form,
            'variables_create_form': variables_create_form,
            'devices_variables_list': devices_variables_list,
            'variables_list': variables_list
        })
        return context


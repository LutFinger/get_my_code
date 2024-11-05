# ----------------------------------------------------------------------------------------------------------------------
# import
from django.urls import path
from . import views

app_name = 'variables'

urlpatterns = [
    path('', views.DevicesAndVariablesView.as_view(), name='variables_list'),
]
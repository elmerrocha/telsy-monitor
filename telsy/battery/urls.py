'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v05.08.2022
Ing. Elmer Rocha Jaime
'''

from django.urls import path
from battery import views

app_name = 'battery'
urlpatterns = [
    path('', views.battery),
]
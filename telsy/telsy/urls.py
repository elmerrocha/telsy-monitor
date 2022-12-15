'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v15.12.2022
Ing. Elmer Rocha Jaime
'''

from django.urls import path, include

app_name = 'telsy'
urlpatterns = [
    path('', include('monitor.urls')),
]

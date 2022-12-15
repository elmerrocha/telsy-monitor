'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v15.12.2022
Ing. Elmer Rocha Jaime
'''

from django.urls import re_path
from monitor.raspberry.measure import Spo2Consumer, NibpConsumer, EcgConsumer, MonitorConsumer, GaugeConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket/spo2', Spo2Consumer.as_asgi()),
    re_path(r'ws/socket/nibp', NibpConsumer.as_asgi()),
    re_path(r'ws/socket/ecg', EcgConsumer.as_asgi()),
    re_path(r'ws/socket/monitor', MonitorConsumer.as_asgi()),
    re_path(r'ws/socket/gauge', GaugeConsumer.as_asgi()),
]
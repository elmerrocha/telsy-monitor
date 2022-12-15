'''
Fundación Cardiovascular de Colombia
Dirección de Innovación y Desarrollo Tecnológico
Proyecto Telsy
Telsy Hogar v15.12.2022
Ing. Elmer Rocha Jaime
'''

from django.urls import path
from monitor import views


app_name = 'monitor'
urlpatterns = [
    path('battery/', views.battery),
    path('connected/',views.Connected.as_view()),
    path('connecting/',views.connecting),
    path('data/', views.data),
    path('exercise/',views.exercise),
    path('goals/',views.goals),
    path('goalsd/',views.goals_details),
    path('goalsv/',views.goals_video),
    path('home/', views.Home.as_view()),
    path('', views.index),
    path('information/', views.information),
    path('login/',views.login),
    path('measure/', views.Measure.as_view()),
    path('medicaments/',views.medicaments),
    path('medicine/',views.medicine),
    path('menu/', views.menu),
    path('monitor/',views.monitor),
    path('monitoring/',views.monitoring),
    path('monitoringinfo/',views.monitoring_info),
    path('monitoringinfov/',views.monitoring_info_video),
    path('network/',views.network),
    path('symptoms/',views.symptoms),
    path('user/', views.user),
    path('weight/',views.weight),
    path('weightc/',views.weight_confirmation),
]
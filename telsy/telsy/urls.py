'''
Fundacion Cardiovascular de Colombia
Proyecto Telsy
Telsy Hogar v07.09.2022
Ing. Elmer Rocha Jaime
'''

"""telsy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from monitor import views

# HTTP Errors to return a custom template
handler400 = 'monitor.views.error_400'
handler403 = 'monitor.views.error_403'
handler404 = 'monitor.views.error_404'
handler500 = 'monitor.views.error_500'

urlpatterns = [
    path('battery/', include('battery.urls')),
    path('cancel/',views.cancel_measurement),
    path('connected/',views.connected),
    path('connecting/<ssid>',views.connecting),
    path('data/',views.data),
    path('exercise/',views.exercise),
    path('goals/',views.goals),
    path('goalsd/',views.goals_details),
    path('goalsv/',views.goals_video),
    path('home/', views.home),
    path('', views.index),
    path('information/', views.information),
    path('login/',views.login),
    path('measuring/',views.measuring),
    path('medicaments/',views.medicaments),
    path('medicine/',views.medicine),
    path('menu/', views.menu),
    path('monitor/',views.monitor),
    path('monitoring/',views.monitoring),
    path('monitoringinfo/',views.monitoring_info),
    path('monitoringinfov/',views.monitoring_info_video),
    path('network/',views.network),
    path('results/',views.results),
    path('symptoms/',views.symptoms),
    path('update/', views.update_monitor),
    path('user/', views.user),
    path('weight/',views.weight),
    path('weightc/',views.weight_confirmation),
]

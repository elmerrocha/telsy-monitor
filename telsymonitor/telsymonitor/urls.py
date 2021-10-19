"""telsymonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from monitor import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cancel/',views.Cancel),
    path('connected/',views.Connected),
    path('connecting/<net>',views.Connecting),
    path('data/',views.Data),
    path('exercise/',views.Exercise),
    path('goals/',views.Goals),
    path('goalsd/',views.GoalsD),
    path('goalsv/',views.GoalsV),
    path('home/', views.Home),
    path('', views.Index),
    path('login/',views.Login),
    path('measuring/',views.Measuring),
    path('medicaments/',views.Medicaments),
    path('medicine/',views.Medicine),
    path('menu/', views.Menu),
    path('monitor/',views.Monitor),
    path('monitoring/',views.Monitoring),
    path('monitoringinfo/',views.MonitoringInfo),
    path('monitoringinfov/',views.MonitoringInfoV),
    path('network/',views.Network),
    path('results/',views.Results),
    path('symptoms/',views.Symptoms),
    path('user/', views.User),
    path('weigth/',views.Weigth),
    path('weigthc/',views.WeigthC),
]

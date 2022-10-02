"""appointmentms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from bookappointment.views import appointment_status, book_appointment, AppointmentAPIView, AppointmentDoctorAPIView, appointment_availablity


urlpatterns = [
    path('admin/', admin.site.urls),
    path('book_appointment/', book_appointment),
    path('appointment_status/', appointment_status),
    path('appointment_availability/', appointment_availablity),
    path('getappointments/<str:pk>/patients/', AppointmentAPIView.as_view()),
    path('getdoctorappointments/<str:pk>/doctors/', AppointmentDoctorAPIView.as_view()),
]

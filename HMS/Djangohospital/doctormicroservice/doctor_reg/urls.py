from django.urls import path
from .views import DoctorRegisterView, DoctorLoginView, DoctorView, DoctorLogoutView, DoctorAPIView
urlpatterns = [
    path('doctorregistration/', DoctorRegisterView.as_view()),
    path('doctorlogin/', DoctorLoginView.as_view()),
    path('doctorview/', DoctorView.as_view()),
    path('doctorlogout/', DoctorLogoutView.as_view()),
    path('doctorapiview/', DoctorAPIView.as_view()),
]

from django.urls import path
from .views import PatientRegisterView, PatientLoginView, PatientView, PatientLogoutView, PatientAPIView, patient_info, PaymentViewAPI
urlpatterns = [
    path('patientregistration/', PatientRegisterView.as_view()),
    path('patientlogin/', PatientLoginView.as_view()),
    path('patientview/', PatientView.as_view()),
    path('patientlogout/', PatientLogoutView.as_view()),
    path('patientinfo/', PatientAPIView.as_view()),
    #path('patient_infos/', PatientAPIInfoView.as_view()),
    #path('patient_infoss/', example),
    path('patient_information/', patient_info),
    path('paymentshistory/', PaymentViewAPI.as_view())
]
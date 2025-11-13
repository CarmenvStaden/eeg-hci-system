from django.urls import path
from dashboards.views import PatientsCreateList, PatientProfileList, PatientDelete

# URLConf
urlpatterns = [
    path('patients/add/', PatientsCreateList.as_view(), name='add_patients'), # add patient (assumes doctor is logged in and performing action)
    path('patients/', PatientsCreateList.as_view(), name='list_patients'), # list logged-in doctor's patients
    path('patients/profiles/all/', PatientProfileList.as_view(), name='list_all_patient_profiles'), # list all patient profiles (testing purposes: looking up patient PROFILE ids)
    path('patients/delete/<int:patient_id>/', PatientDelete.as_view(), name='delete_patient')
]
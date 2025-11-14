from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    email = models.EmailField(unique=True) # replaces username as unique identifier
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

# profiles created 
class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="doctor_profile") # related_name for reverse relation
    specialization = models.CharField(max_length=100, blank=True, null=True)

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="patient_profile") # related_name for reverse relation
    date_of_birth = models.DateField(blank=True, null=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="patients") # associates a patient to a doctor -> for doctors to view list of patients
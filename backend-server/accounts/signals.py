from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, DoctorProfile, PatientProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal automatically assigns a CustomUser as a "is_doctor" or "is_patient" profile upon creation.
    """
    # profile created when role assigned in UserRoleUpdate by Admin
    if instance.is_doctor and not hasattr(instance, "doctorprofile"):
        DoctorProfile.objects.create(user=instance)

    if instance.is_patient and not hasattr(instance, "patientprofile"):
        PatientProfile.objects.create(user=instance)
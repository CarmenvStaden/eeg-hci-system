from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, DoctorProfile, PatientProfile

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal automatically assigns a CustomUser as a "is_doctor" or "is_patient" profile upon creation.
    """
    if created:
        if instance.is_doctor:
            DoctorProfile.objects.create(user=instance)
        elif instance.is_patient:
            PatientProfile.objects.create(user=instance)
from django.db import models
from django.conf import settings

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=100) # should describe what being tested
    description = models.TextField(blank=True, null=True)
    # possible level details?

class Prescription(models.Model): # connects doctor to patient through game
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prescriptions_made")
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="prescriptions_received")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

class Session(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions")
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True) 

class EEGReading(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="eeg_readings")
    timestamp = models.DateTimeField()
    attention = models.FloatField()
    meditation = models.FloatField()
    delta = models.FloatField()
    theta = models.FloatField()
    low_alpha = models.FloatField()
    high_alpha = models.FloatField()
    low_beta  = models.FloatField()
    high_beta  = models.FloatField()
    low_gamma = models.FloatField()
    mid_gamma = models.FloatField()

class Report(models.Model):
    session = models.OneToOneField(Session, on_delete=models.CASCADE, related_name="report")
    created_at = models.DateTimeField(auto_now_add=True)
    # what will the report look like and how will it be stored?
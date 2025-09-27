from django.db import models
from django.conf import settings

# Create your models here.
class Session(models.Model):
    user = models.ForeignKey( # Foreign key = one-to-many relationship
        settings.AUTH_USER_MODEL, # references user model
        on_delete=models.CASCADE, # if user deleted, all associated model instances deleted
        related_name="sessions" # for reverse lookup
        ) 
    game_type = models.CharField(max_length=20)
    game_level = models.IntegerField()
    start_time   = models.DateTimeField(auto_now_add=True)
    end_time     = models.DateTimeField(null=True, blank=True)

class EEGReading(models.Model):
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE, 
        related_name="readings")
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
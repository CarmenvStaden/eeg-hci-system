from rest_framework import serializers
from .models import Session, EEGReading

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["id", "user", "game_type", "game_level",
                  "start_time", "end_time"]
        read_only_fields = ["id", "user", "start_time"] # not set by client

class EEGReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EEGReading
        fields = ["id", "session", "timestamp",
                  "attention", "meditation",
                  "delta", "theta", "low_alpha", "high_alpha",
                  "low_beta", "high_beta", "low_gamma", "mid_gamma"]
        read_only_fields = ["id", "session"]
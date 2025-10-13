from rest_framework import serializers
from .models import Session, EEGReading, Game, Prescription

class EEGReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EEGReading
        fields = ["id", "session", "timestamp", 
                  "attention", "meditation",
                  "delta", "theta", "low_alpha", "high_alpha",
                  "low_beta", "high_beta", "low_gamma", "mid_gamma"]
        read_only_fields = ["id"] # include "session" if Unity POST doesn't already include the session id

class SessionSerializer(serializers.ModelSerializer):
    eeg_readings = EEGReadingSerializer(many=True, read_only=True)
    
    class Meta:
        model = Session
        fields = ["id", "user", "game_type", "game_level",
                  "start_time", "end_time", "eeg_readings"]
        # read_only_fields = ["id", "user", "start_time"] # not set by client

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["id", "doctor", "patient", "game", "notes", "created_at", "active"]
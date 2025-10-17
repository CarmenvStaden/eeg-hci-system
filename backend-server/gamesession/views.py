from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session, EEGReading, Prescription
from .serializers import SessionSerializer, EEGReadingSerializer, PrescriptionSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

# Create an EEG-Reading instance (unity POSTs here -> serializer -> model with all data -> DB)
class EEGReadingCreateView(APIView):
    def post(self, request): 
        serializer = EEGReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Start a session    
class SessionStartView(APIView):
    def post(self, request): # incoming: Unity -> server
        patient = request.user
        game_id = request.data.get("game_id")
        prescription_id = request.data.get("prescription_id", None)

        session = Session.objects.create(
            patient=patient,
            game_id=game_id,
            prescription_id=prescription_id,
            start_time=timezone.now()
        )
        serializer = SessionSerializer(session).data # deserialize: JSON -> django model instance
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# End a session
class SessionEndView(APIView):
    def post(self, request, session_id):
        try:
            session = Session.objects.get(id=session_id)
            session.end_time = timezone.now()
            session.save()
            return Response(SessionSerializer(session).data)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)
        
# Prescription Views
class PrescriptionListCreateView(APIView):
    """
    Only authenticated users can see list of games (GET). Only specialists can assign games (POST).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request): # outgoing: server -> client
        if request.user.is_doctor:
            prescriptions = Prescription.objects.filter(doctor=request.user) # list prescriptions a doctor has assigned
        else:
            prescriptions = Prescription.objects.filter(patient=request.user) # list prescriptions a patient has been assigned
        serializer = PrescriptionSerializer(prescriptions, many=True) # serialize the list to JSON for outgoing responses to client
        return Response(serializer.data)

    def post(self, request): # incoming: client -> server
        if not request.user.is_doctor:
            return Response({"error": "Only specialists can assign games"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = PrescriptionSerializer(data=request.data) # deserialize list from client (JSON) to server (model instance)
        if serializer.is_valid(): # if matches formatting in models
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
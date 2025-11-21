from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session, EEGReading, Prescription, Game
from accounts.models import CustomUser
from .serializers import SessionSerializer, EEGReadingSerializer, PrescriptionSerializer, GameSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

class GameListCreateView(APIView): 
    """
    Returns a list of games (GET).
    Creates a game (POST) from the model.
    """
    def get(self, request):
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Prescription Views
class PrescriptionListCreateView(APIView):
    """
    Users must be authenticated (logged in).
    Returns a list of games (GET). 
        Specialists see the games they assigned to Patients.
        Patients see the games they were assigned by Specialists. 
    Only specialists can create/assign games (POST).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request): # outgoing: server -> client
        if request.user.is_doctor:
            prescriptions = Prescription.objects.filter(doctor=request.user) 
        else:
            prescriptions = Prescription.objects.filter(patient=request.user) 
        serializer = PrescriptionSerializer(prescriptions, many=True) # serialize the list to JSON for outgoing responses to client
        return Response(serializer.data)

    def post(self, request): # incoming: client -> server
        if not (request.user.is_authenticated and request.user.is_doctor):
            return Response({"error": "Only doctors can create prescriptions."},
                        status=status.HTTP_403_FORBIDDEN)
        
        serializer = PrescriptionSerializer(data=request.data) # deserialize list from client (JSON) to server (model instance)
        if serializer.is_valid(): # if matches formatting in models
            serializer.save(doctor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SessionListCreateView(APIView):
    def get(self, request):
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetSessionByUserIDDoctor(APIView):
    """
    For doctors.
    Returns list of all sessions associated to the ID of the patient passed into the URL.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, target_patient_id):
        user = request.user

        if not user.is_doctor:
            return Response("doctor only action", status=status.HTTP_403_FORBIDDEN)

        try:
            target_user = CustomUser.objects.get(id=target_patient_id)
        except CustomUser.DoesNotExist:
            return Response({"error": f"record with ID {target_patient_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if target_user.is_doctor:
            return Response("cannot view other doctors' sessions", status=status.HTTP_403_FORBIDDEN)
        
        sessions = target_user.sessions.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetMySession(APIView):
    """
    For patients.
    Returns list of all sessions associated to the logged-in patient.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_patient:
            return Response("patient only action", status=status.HTTP_403_FORBIDDEN)
        
        sessions = user.sessions.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Start a session    
class SessionStartView(APIView):
    """
    Starts a session for authenticated patients (logged-in). 
    Requires game_id in body (prescription_id optional, but recommended).
    Creates a Session object from data, including current time. 
    """
    def post(self, request): # incoming: Unity -> server
        permission_classes = [IsAuthenticated] # must be logged in

        patient = request.user # automatically assigned if user logged in
        game_id = request.data.get("game_id") # in body
        prescription_id = request.data.get("prescription_id", None) # in body

        session = Session.objects.create(
            patient=patient,
            game_id=game_id,
            prescription_id=prescription_id,
            start_time=timezone.now()
        )
        serializer = SessionSerializer(session).data # deserialize: JSON -> django model instance
        return Response(serializer, status=status.HTTP_201_CREATED)

# End a session
class SessionEndView(APIView):
    """
    Ends a session. 
    Expects the session_id of a created session. 
    Saves an end time for to that Session object; otherwise, returns error if not found.
    """
    def post(self, request, session_id): # session_id in header
        try:
            session = Session.objects.get(id=session_id)
            session.end_time = timezone.now()
            session.save()
            return Response(SessionSerializer(session).data)
        except Session.DoesNotExist:
            return Response({"error": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

# Create an EEG-Reading instance (unity POSTs here -> serializer -> model with all data -> DB)
class EEGReadingCreateView(APIView):
    """
    Lists all EEG-Readings, currently for testing purposes (GET).
    Creates an EEG-Reading object out of the incoming data from Unity (POST). 
    """
    def get(self, request):
        readings = EEGReading.objects.all()
        serializer = EEGReadingSerializer(readings, many=True)
        return Response(serializer.data)

    def post(self, request): 
        serializer = EEGReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetEEGBySessionIDDoctor(APIView):
    """
    For doctors.
    Returns all the eeg-readings of a particular session (target_session_id) by a particular patient (target_user_id).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, target_session_id, target_patient_id):
        user = request.user

        if not user.is_doctor:
            return Response("doctor only action", status=status.HTTP_403_FORBIDDEN)
        
        try:
            target_user = CustomUser.objects.get(id=target_patient_id)
        except CustomUser.DoesNotExist:
            return Response({"error": f"record with ID {target_patient_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if target_user.is_doctor:
            return Response("cannot view other doctors' sessions", status=status.HTTP_403_FORBIDDEN)

        try:
            target_session = Session.objects.get(id=target_session_id, patient=target_user)
        except Session.DoesNotExist:
            return Response({"error": f"session with ID {target_session_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        eeg_readings = target_session.egg_readings.all()
        serializer = EEGReadingSerializer(eeg_readings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetMyEEGBySession(APIView):
    """
    For patients.
    Returns list of a patient's own eeg-readings associated to a particular session.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, target_session_id):
        user = request.user

        if not user.is_patient:
            return Response("patient only action", status=status.HTTP_403_FORBIDDEN)
        
        try:
            target_session = Session.objects.get(id=target_session_id, patient=user)
        except Session.DoesNotExist:
            return Response({"error": f"session with ID {target_session_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        eeg_readings = target_session.eeg_readings.all()
        serializer = EEGReadingSerializer(eeg_readings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
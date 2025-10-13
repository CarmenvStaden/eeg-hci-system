from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Session, EEGReading
from .serializers import SessionSerializer, EEGReadingSerializer
from django.utils import timezone

# Create an EEG-Reading instance (unity POSTs here -> serializer -> model with all data -> DB)
class EEGReadingCreateView(APIView):
    def post(self, request, *args, **kwargs): 
        serializer = EEGReadingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Start a session    
class SessionStartView(APIView):
    def post(self, request):
        patient = request.user
        game_id = request.data.get("game_id")
        prescription_id = request.data.get("prescription_id", None)

        session = Session.objects.create(
            patient=patient,
            game_id=game_id,
            prescription_id=prescription_id,
            start_time=timezone.now()
        )
        return Response(SessionSerializer(session).data, status=status.HTTP_201_CREATED)

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
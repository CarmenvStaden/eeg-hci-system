from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Session, EEGReading
from .serializers import SessionSerializer, EEGReadingSerializer

# Create your views here.
class EEGReadingViewSet(viewsets.ModelViewSet):
    queryset = EEGReading.objects.all()
    serializer_class = EEGReadingSerializer

    # /api/eeg-readings/by-session/<session_id>/
    @action(detail=False, url_path='by-session/(?P<session_id>[^/.]+)')
    def by_session(self, request, session_id=None):
        readings = EEGReading.objects.filter(session=session_id).order_by('timestamp')
        serializer = self.get_serializer(readings, many=True)
        return Response(serializer.data)

class SessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
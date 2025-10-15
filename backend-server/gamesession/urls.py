from django.urls import path
from gamesession.views import EEGReadingCreateView, SessionStartView, SessionEndView, PrescriptionListCreateView

# /gamesessions/...
urlpatterns = [
    path('eeg-readings/', EEGReadingCreateView.as_view(), name="eeg-reading-create"), # where Unity streams eeg-data
    path('sessions/start/', SessionStartView.as_view(), name='session-start'), # start a session
    path('sessions/<int:session_id>/end/', SessionEndView.as_view(), name='session-end'), # end a session
    path("prescriptions/", PrescriptionListCreateView.as_view(), name="prescription-list-create"), # read/list (get) or create (post) prescriptions (house games)
]
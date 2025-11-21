from django.urls import path
from gamesession.views import EEGReadingCreateView, SessionStartView, SessionEndView, PrescriptionListCreateView, GameListCreateView, SessionListCreateView, GetMySession, GetSessionByUserIDDoctor

# /gamesessions/...
urlpatterns = [
    path('games/', GameListCreateView.as_view(), name='game-list-create'),
    path("prescriptions/", PrescriptionListCreateView.as_view(), name="prescription-list-create"), # read/list (get) or create (post) prescriptions (house games)
    path('sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/start/', SessionStartView.as_view(), name='session-start'), # start a session
    path('sessions/<int:session_id>/end/', SessionEndView.as_view(), name='session-end'), # end a session
    path('eeg-readings/', EEGReadingCreateView.as_view(), name="eeg-reading-create"), # where Unity streams eeg-data
    path('sessions/me/',GetMySession.as_view(), name='get_my_sessions'),
    path('sessions/<int:target_patient_id>/', GetSessionByUserIDDoctor.as_view(), name='get_sessions_by_user_id')
]
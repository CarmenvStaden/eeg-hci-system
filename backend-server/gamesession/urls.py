from django.urls import path
from gamesession.views import EEGReadingCreateView, SessionStartView, SessionEndView, PrescriptionListCreateView, GameListCreateView, SessionListCreateView

# /gamesessions/...
urlpatterns = [
    path('games/', GameListCreateView.as_view(), name='game-list-create'),
    path("prescriptions/", PrescriptionListCreateView.as_view(), name="prescription-list-create"), # read/list (get) or create (post) prescriptions (house games)
    path('sessions/', SessionListCreateView.as_view(), name='session-list-create'),
    path('sessions/start/', SessionStartView.as_view(), name='session-start'), # start a session
    path('sessions/<int:session_id>/end/', SessionEndView.as_view(), name='session-end'), # end a session
    path('eeg-readings/', EEGReadingCreateView.as_view(), name="eeg-reading-create"), # where Unity streams eeg-data
]
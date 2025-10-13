from django.urls import path
from gamesession.views import EEGReadingCreateView, SessionStartView, SessionEndView

# /gamesessions/...
urlpatterns = [
    path('eeg-readings/', EEGReadingCreateView.as_view(), name="eeg-reading-create"), # where Unity streams eeg-data
    path('sessions/start/', SessionStartView.as_view(), name='session-start'), # start a session
    path('sessions/<int:session_id>/end/', SessionEndView.as_view(), name='session-end'), # end a session
]
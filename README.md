# eeg-hci-system
A human-computer interface that utilizes EEG data generated from gameplay for analysis and observation of potential mental disorders.

## BACKEND
### Prerequisites
- Python 3.x installed  
- pip or homebrew
- pipenv (`pip install --user pipenv` OR `brew install pipenv`)

### Initial Start (at beginning)

_Clone the Repo_  

`git clone https://github.com/CarmenvStaden/eeg-hci-system.git`  
`cd eeg-hci-system/backend-server`

 ### Daily Development (from backend-server directory)  

_Create/Activate the virtual environment_  

`pipenv shell`

_Install from Pipfile (for development, allowing resolution of new dependencies)_  

`pipenv install`

_Apply Database Migrations_  

`python manage.py migrate`

 _Create Superuser (only once for initial setup)_  

`python manage.py createsuperuser`

 _Run Dev Server_  

`python manage.py runserver`
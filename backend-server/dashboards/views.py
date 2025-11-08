from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import DoctorProfile, PatientProfile, CustomUser
from .serializers import PatientAddSerializer, DoctorSerializer, PatientSerializer
# from .serializers import 
from rest_framework.permissions import IsAuthenticated

class PatientProfileList(APIView):
    """
    Returns list of patient profiles with corresponding id, email, and username.
    """
    def get(self, request):
        patient_profiles = PatientProfile.objects.all()
        serializer = PatientSerializer(patient_profiles, many=True)
        return Response(serializer.data)

# Create your views here.
class PatientsCreateList(APIView):
    """
    Allows logged-in doctor to add (post) and list (get) patients. Assumes the doctor performing the action is logged in.
    Expects a PatientProfile id (post).
    Post: returns a success message if patient is correctly associated to a doctor, or error otherwise.
    Get: returns a list of doctor's patients
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PatientAddSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            patient_profile = serializer.save()
            return Response({f"patient {patient_profile.user.email} assigned to doctor."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user # should the logged in user
        
        if not user.is_doctor: # is_doctor is an attribute of the CustomUser model
            return Response("only doctors can see their patient lists", status=status.HTTP_403_FORBIDDEN)
        
        doctor = DoctorProfile.objects.filter(user=user).first() # return first instance of matching user
        if not doctor:
            return Response("doctor could not be found")
        
        patients = doctor.patients.all() # gets all patients related to the logged in doctor; reverse relation
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
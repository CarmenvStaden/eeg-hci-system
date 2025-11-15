from rest_framework import serializers
from accounts.models import DoctorProfile, PatientProfile, CustomUser

class PatientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = PatientProfile
        fields = ['id', 'email', 'username', 'date_of_birth']

# just in case, for later allowing doctors to add to 'specialization' field
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'specialization']

class PatientAddSerializer(serializers.Serializer):
    """
    Creates Doctor and Patient Profiles for patient-doctor relationship from CustomUser model is_doctor or is_patient tags.
    """
    # accept the patient by CustomUser.ID -> will become CustomUser.is_patient.ID once verified
    patient_user_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        """
        Only doctors (logged in) can add patients.
        """
        user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError("not authenticated")

        if not user.is_doctor:
            raise serializers.ValidationError({"doctor_role_error": "only doctors can add patients."})

        # either DoctorProfile exists, otherwise create at first instance of trying to add a patient
        DoctorProfile.objects.get_or_create(user=user)

        # double check that patient exists based off CustomUser.ID (passed in as patient_user_id)
        patient_user_id = attrs.get('patient_user_id')
        try:
            patient_user = CustomUser.objects.get(id=patient_user_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"invalid_id_error": f"no such user with id {patient_user_id} exists."})

        # make sure that if CustomUser.ID (named patient_user_id) is valid, has an 'is_patient' tag
        if not patient_user.is_patient:
            raise serializers.ValidationError({"patient_role_error": "user is not a patient."})
        
        # ensure PatientProfile exists, otherwise create at first instance of being added to doctor
        patient_profile, _ = PatientProfile.objects.get_or_create(user=patient_user)

        attrs['patient_profile'] = patient_profile
        return attrs

    def create(self, validated_data):
        doctor_profile = self.context['request'].user.doctor_profile # user.doctor_profile directly accesses from CustomUser instance the DoctorProfile
        patient_profile = validated_data['patient_profile'] # reverse relation
        patient_profile.doctor = doctor_profile # establishes the patient-doctor relationship through profiles
        patient_profile.save()
        return patient_profile
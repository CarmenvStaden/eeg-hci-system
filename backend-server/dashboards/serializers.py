from rest_framework import serializers
from accounts.models import DoctorProfile, PatientProfile

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
    # accept the patient by PatientProfile.id
    patient_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        """
        Only doctors (logged in) can add patients.
        """
        user = self.context['request'].user

        if not user.is_authenticated:
            raise serializers.ValidationError("not authenticated")

        if not user.is_doctor:
            raise serializers.ValidationError("only doctors can add patients.")

        # double check that DoctorProfile exists
        DoctorProfile.objects.get_or_create(user=user)

        # double check that patient exists
        patient_id = attrs.get('patient_id')
        try:
            patient_profile = PatientProfile.objects.get(id=patient_id)
        except PatientProfile.DoesNotExist:
            raise serializers.ValidationError(f"Patient with id {patient_id} does not exist.")

        attrs['patient_profile'] = patient_profile  # attach for create()
        return attrs

    def create(self, validated_data):
        doctor = self.context['request'].user.doctor_profile # user.doctor_profile directly accesses from CustomUser instance the DoctorProfile
        patient_profile = validated_data['patient_profile'] # reverse relation
        patient_profile.doctor = doctor # corresponds a doctor to a patient
        patient_profile.save()
        return patient_profile
from rest_framework import serializers
from .models import User, FacilityDetails, WasteType, DisposalDetails, RequestStatus, FormDetails


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class FacilityDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacilityDetails
        fields = ['bldg_no', 'facility_name']

class WasteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteType
        fields = ['sl_no', 'bldg_no', 'waste_type']

class RequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestStatus
        fields = '__all__'


class FormDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDetails
        fields = '__all__'


class DisposalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisposalDetails
        fields = '__all__'
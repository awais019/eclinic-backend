from django.core.validators import MinValueValidator
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import Doctor, Patient, Location, Review
from datetime import date

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'lat', 'lng', 'address', 'city', 'state']
    # lat = serializers.DecimalField(max_digits=9, decimal_places=6)
    # lng = serializers.DecimalField(max_digits=9, decimal_places=6)
    # address = serializers.CharField(max_length=255)
    # city = serializers.CharField(max_length=255)
    # state = serializers.CharField(max_length=255)

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'first_name', 'last_name',
                  'email', 'phone_number', 'gender', 'password']
    
    id = serializers.IntegerField(read_only=True)

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name','email', 'phone_number', 'gender']

class DoctorSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'password', 
                  'specialization', 'charges', 'location']
    location = LocationSerializer()
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255, source='user.first_name')
    last_name = serializers.CharField(max_length=255, source='user.last_name')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(max_length=20, source='user.phone_number')
    gender = serializers.CharField(max_length=20, source='user.gender')
    password = serializers.CharField(write_only=True, source='user.password')
    specialization = serializers.CharField(max_length=255)
    charges = serializers.DecimalField(max_digits=8, decimal_places=2,
                                        validators=[MinValueValidator(1)])
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user.save()
        location = validated_data.pop('location')
        location = Location.objects.create(**location)
        return Doctor.objects.create(user=user.instance, location=location, **validated_data)

    # first_name = serializers.CharField(max_length=255)
    # last_name = serializers.CharField(max_length=255)
    # email = serializers.EmailField()
    # phone_number = serializers.CharField(max_length=20)
    # specialization = serializers.CharField(max_length=255)
    # gender = serializers.CharField(max_length=20)
    # charges = serializers.DecimalField(max_digits=8, decimal_places=2,
    #                                    validators=[MinValueValidator(1)])


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'gender', 'specialization', 'charges']
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=20)

    def update(self, instance, validated_data):
        user_data = {
            'first_name': validated_data.get('first_name', instance.user.first_name),
            'last_name': validated_data.get('last_name', instance.user.last_name),
            'gender': validated_data.get('gender', instance.user.last_name),
            'email': instance.user.email,
            'phone_number': instance.user.phone_number,
            'password': instance.user.password
        }
        user = UserSerializer(instance.user, data=user_data)
        user.is_valid(raise_exception=True)
        user.save()
        return super().update(instance, validated_data)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'phone_number', 'password', 'birth_date']

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255, source='user.first_name')
    last_name = serializers.CharField(max_length=255, source='user.last_name')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(max_length=20, source='user.phone_number')
    gender = serializers.CharField(max_length=20, source='user.gender')
    password = serializers.CharField(write_only=True, source='user.password')
    birth_date = serializers.DateField()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user.save()
        return Patient.objects.create(user=user.instance, **validated_data)
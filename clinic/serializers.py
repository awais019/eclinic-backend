from django.core.validators import MinValueValidator
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import Doctor, Patient, Location, Review, User

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
                  'email', 'phone_number', 'gender', 'password', 'user_type']
    
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
        user_data['user_type'] = 'doctor'
        user = UserCreateSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user.save()
        location = validated_data.pop('location')
        location = Location.objects.create(**location)
        return Doctor.objects.create(user=user.instance, location=location, **validated_data)

    def update(self, instance, validated_data):
        print(validated_data)
        if validated_data.get('email'):
            raise serializers.ValidationError("You can't change email")
        elif validated_data.get('phone_number'):
            raise serializers.ValidationError("You can't change phone number")
        elif validated_data.get('password'):
            raise serializers.ValidationError("You can't change password")
        
        return super().update(instance, validated_data)

    # first_name = serializers.CharField(max_length=255)
    # last_name = serializers.CharField(max_length=255)
    # email = serializers.EmailField()
    # phone_number = serializers.CharField(max_length=20)
    # specialization = serializers.CharField(max_length=255)
    # gender = serializers.CharField(max_length=20)
    # charges = serializers.DecimalField(max_digits=8, decimal_places=2,
    #                                    validators=[MinValueValidator(1)])


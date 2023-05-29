from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import Doctor, Patient, Location, Review, Appointment, UserImage, User
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

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'image']

    def create(self, validated_data):
        user_id = self.context['user_id']
        user = User.objects.get(id=user_id)
        return UserImage.objects.create(user=user, **validated_data)

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'last_name','email', 'phone_number', 'gender', 'image']


class DoctorSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'gender', 'password', 
                  'specialization', 'charges', 'image_url', 'location']
    location = LocationSerializer()
    image_url = serializers.SerializerMethodField(read_only=True, method_name='get_image')
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
    
    def get_image(self, obj):
        if UserImage.objects.filter(user_id=obj.user.id).exists():
            request = self.context.get('request')
            return request.build_absolute_uri(UserImage.objects.get(user_id=obj.user.id).image.url)
        return None

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
        fields = ['id', 'first_name', 'last_name', 'gender', 'email', 'phone_number', 'password', 'birth_date', 'age', 'image']

    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255, source='user.first_name')
    last_name = serializers.CharField(max_length=255, source='user.last_name')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(max_length=20, source='user.phone_number')
    gender = serializers.CharField(max_length=20, source='user.gender')
    password = serializers.CharField(write_only=True, source='user.password')
    birth_date = serializers.DateField()
    age = serializers.SerializerMethodField(read_only=True, method_name='cal_age')
    image = serializers.SerializerMethodField(read_only=True, method_name='get_image')

    def cal_age(self, obj):
        today = date.today()
        age = today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
        if age > 0:
            return f'{age} years'
        age = (today.month - obj.birth_date.month) % 12
        if age > 0:
            return f'{age} months'
        age = (today.day - obj.birth_date.day) % 30
        return f'{age} days'

    def get_image(self, obj):
        if UserImage.objects.filter(user_id=obj.user.id).exists():
            request = self.context.get('request')
            return request.build_absolute_uri(UserImage.objects.get(user_id=obj.user.id).image.url)
        return None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserCreateSerializer(data=user_data)
        user.is_valid(raise_exception=True)
        user.save()
        return Patient.objects.create(user=user.instance, **validated_data)
    
class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'gender', 'birth_date']
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    gender = serializers.CharField(max_length=20)
    birth_date = serializers.DateField()

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
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'patient', 'patient_name', 'rating', 'review', 'date']
    id = serializers.IntegerField(read_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.select_related().all())
    patient_name = serializers.SerializerMethodField(read_only=True, method_name='get_patient_name')
    rating = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = serializers.CharField(max_length=255, allow_blank=True)
    date = serializers.DateTimeField(read_only=True, format='%d-%m-%Y %H:%M:%S')

    def get_patient_name(self, obj):
        return f'{obj.patient.user.first_name} {obj.patient.user.last_name}'

    def create(self, validated_data):
        doctor_id = self.context['view'].kwargs['doctors_pk']
        doctor = Doctor.objects.get(id=doctor_id)
        return Review.objects.create(doctor=doctor, **validated_data)
    
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'time']
    
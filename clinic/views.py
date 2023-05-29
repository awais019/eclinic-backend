from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
import jwt
from rest_framework.filters import SearchFilter, OrderingFilter

from .filtering import DoctorFilter
from .pagination import DefaultPagination
from .models import Doctor, User, Patient, Review, Appointment, UserImage
from .serializers import DoctorSerializer, DoctorUpdateSerializer, PatientSerializer, \
                        PatientUpdateSerializer, ReviewSerializer, AppointmentSerializer, \
                            UserImageSerializer, TokenSerializer
# Create your views here.
def index(request):
    return render(request, 'index.html')


class UserProfileViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        is_doctor = Doctor.objects.filter(user_id=self.request.user.id).exists()
        is_patient = Patient.objects.filter(user_id=self.request.user.id).exists()
        if is_doctor:
            if self.request.method == 'PUT':
                return DoctorUpdateSerializer
            return DoctorSerializer
        elif is_patient:
            if self.request.method == 'PUT':
                return PatientUpdateSerializer
            return PatientSerializer
        
    def get_serializer_context(self):
        return {
            'request': self.request,
        }

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        is_doctor = Doctor.objects.filter(user_id=request.user.id).exists()
        is_patient = Patient.objects.filter(user_id=request.user.id).exists()
        context = self.get_serializer_context()
        if is_doctor:
            doctor = Doctor.objects.get(user_id=request.user.id)
            if request.method == 'GET':
                serializer = DoctorSerializer(doctor, context=context)
                return Response(serializer.data)
            if request.method == 'PUT':
                serializer = DoctorUpdateSerializer(doctor, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        elif is_patient:
            patient = Patient.objects.get(user_id=request.user.id)
            if request.method == 'GET':
                serializer = PatientSerializer(patient, context=context)
                return Response(serializer.data)
            if request.method == 'PUT':
                serializer = PatientUpdateSerializer(patient, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        

class DoctorRegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorListViewSet(ListModelMixin, GenericViewSet):
    queryset = Doctor.objects.select_related().all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DoctorFilter
    search_fields = ['user__first_name', 'user__last_name', 'location__address', 'location__city', 'location__state']
    ordering_fields = ['user__first_name', 'user__last_name', 'charges']
    pagination_class = DefaultPagination

class DoctorRetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Doctor.objects.select_related().all()
    serializer_class = DoctorSerializer

class PatientRegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class PatientRetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Patient.objects.select_related().all()
    serializer_class = PatientSerializer

class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related().all()
    serializer_class = ReviewSerializer

class AppointmentViewSet(CreateModelMixin, GenericViewSet):
    queryset = Appointment.objects.select_related().all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        is_patient = Patient.objects.filter(user_id=request.user.id).exists()
        if is_patient:
            if Appointment.objects.filter(patient=request.data['patient'], date=request.data['date']).filter(doctor=request.data['doctor']).exists():
                return Response({'error': 'You already have an appointment on the same date.'}, status=400)
            if Appointment.objects.filter(doctor=request.data['doctor'], date=request.data['date'], time=request.data['time']).exists():
                return Response({'error': 'Doctor is not available at this time.'}, status=400)
            
            return super().create(request, *args, **kwargs)
        
        return Response({'error': 'Only patients can create appointments.'}, status=403)
        

class UserImageViewSet(ModelViewSet):
    serializer_class = UserImageSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id
        }

    def get_queryset(self):
        return UserImage.objects.filter(user_id=self.request.user.id)
    
    def create(self, request, *args, **kwargs):
        if UserImage.objects.filter(user_id=request.user.id).exists():
            UserImage.objects.filter(user_id=request.user.id).delete()
        return super().create(request, *args, **kwargs)
    

class VerifyUserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = TokenSerializer

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        token = request.data.get('token')
        print(token)
        if token is None:
            return Response({'error': 'Token is required'}, status=400)
        try:
            decode_token = jwt.decode(token, key='secret', algorithms=['HS256'])
            user = User.objects.get(id=decode_token['user_id'])
            if user.is_active:
                return Response({'error': 'User already verified'}, status=400)
            user.is_active = True
            user.save()
            return Response({'message': 'User verified successfully'}, status=200)
        except:
            return Response({'error': 'Invalid token'}, status=400)
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .filtering import DoctorFilter
from .pagination import DefaultPagination
from .models import Doctor, User, Patient, Review
from .serializers import DoctorSerializer, DoctorUpdateSerializer, PatientSerializer, \
                        PatientUpdateSerializer, ReviewSerializer
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

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        is_doctor = Doctor.objects.filter(user_id=request.user.id).exists()
        is_patient = Patient.objects.filter(user_id=request.user.id).exists()
        if is_doctor:
            doctor = Doctor.objects.get(user_id=request.user.id)
            if request.method == 'GET':
                serializer = DoctorSerializer(doctor)
                return Response(serializer.data)
            if request.method == 'PUT':
                serializer = DoctorUpdateSerializer(doctor, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
        elif is_patient:
            patient = Patient.objects.get(user_id=request.user.id)
            if request.method == 'GET':
                serializer = PatientSerializer(patient)
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
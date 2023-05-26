from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import Doctor, User
from .serializers import DoctorSerializer, DoctorUpdateSerializer
# Create your views here.

def index(request):
    return render(request, 'index.html')


class UserProfileViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        is_doctor = Doctor.objects.filter(user_id=self.request.user.id).exists()
        if is_doctor:
            if self.request.method == 'PUT':
                return DoctorUpdateSerializer
            return DoctorSerializer

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        is_doctor = Doctor.objects.filter(user_id=request.user.id).exists()
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
        

class DoctorRegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
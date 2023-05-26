from django.shortcuts import render

from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Doctor
from .serializers import DoctorSerializer
# Create your views here.

def index(request):
    return render(request, 'index.html')


class DoctorRegisterViewSet(CreateModelMixin, GenericViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
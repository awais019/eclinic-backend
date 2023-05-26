from django_filters.rest_framework import FilterSet
from .models import Doctor

class DoctorFilter(FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'approval_status': ['exact'],
            'specialization': ['exact'],
            'charges': ['gte', 'lte'],
        }
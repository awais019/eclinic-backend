from django_filters.rest_framework import FilterSet
from .models import Doctor

class DoctorFilter(FilterSet):
    class Meta:
        model = Doctor
        fields = {
            'specialization': ['iexact'],
            'charges': ['gte', 'lte'],
        }
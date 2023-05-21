from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Doctor)
admin.site.register(models.Patient)
admin.site.register(models.Appointment)
admin.site.register(models.Prescription)
admin.site.register(models.Review)
admin.site.register(models.Payment)
admin.site.register(models.MedicalRecord)

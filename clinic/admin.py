from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'specialization', 'email', 'phone_number', 
                    'charges', 'location', 'status', 'approval_status']
    list_per_page = 10
    list_editable = ['status', 'approval_status']
    list_select_related = ['location']
    def location(self, doctor):
        return doctor.location.address + ", " + doctor.location.city + ", " + doctor.location.state
    

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'email', 'phone_number']
    list_per_page = 10

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'state']
    list_per_page = 10

@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time', 'approval']
    list_per_page = 10

@admin.register(models.Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'prescription']
    list_per_page = 10

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'rating', 'review']
    list_per_page = 10

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'amount', 'paid', 'payment_method']
    list_editable = ['paid']
    list_per_page = 10

@admin.register(models.MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'symptoms', 'diagnosis']
    list_per_page = 10
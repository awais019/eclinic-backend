from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'phone_number', 'is_staff']
    ordering = ['email', 'first_name', 'last_name', 'date_joined']
    fieldsets = (
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", 
                           "phone_number", "first_name", "last_name", "gender"),
            },
        ),
    )

@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name', 'specialization', 'email', 'phone_number', 
                    'charges', 'location', 'approval_status']
    list_per_page = 10
    list_editable = ['approval_status']
    list_select_related = ['location']
    search_fields = ['first_name__istartswith', 'last_name__istartswith', 'specialization__istartswith']    
    list_filter = ['approval_status', 'specialization']
    def location(self, doctor):
        return doctor.location.address + ", " + doctor.location.city + ", " + doctor.location.state
    

@admin.register(models.Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'gender', 'email', 'phone_number']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'state']
    list_per_page = 10
    search_fields = ['address__istartswith', 'city__istartswith', 'state__istartswith']
    list_filter = ['city', 'state']

@admin.register(models.Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'time', 'approval']
    list_per_page = 10
    search_fields = ['patient__first_name__istartswith', 'patient__last_name__istartswith',
                     'doctor__first_name__istartswith', 'doctor__last_name__istartswith']
    list_filter = ['approval', 'date', 'time']

@admin.register(models.Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'date', 'prescription']
    list_per_page = 10
    search_fields = ['patient__first_name__istartswith', 'patient__last_name__istartswith',
                     'doctor__first_name__istartswith', 'doctor__last_name__istartswith']

@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'rating', 'review']
    list_per_page = 10
    search_fields = ['patient__first_name__istartswith', 'patient__last_name__istartswith',
                     'doctor__first_name__istartswith', 'doctor__last_name__istartswith',
                     'review__istartswith']
    list_filter = ['rating']

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'amount', 'paid', 'payment_method']
    list_editable = ['paid']
    list_per_page = 10
    search_fields = ['appointment__patient__first_name__istartswith',
                     'appointment__patient__last_name__istartswith',
                     'appointment__doctor__first_name__istartswith',
                     'appointment__doctor__last_name__istartswith']
    list_filter = ['paid']

@admin.register(models.MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'symptoms', 'diagnosis']
    list_per_page = 10
    search_fields = ['prescription__patient__first_name__istartswith',
                     'prescription__patient__last_name__istartswith',
                     'prescription__doctor__first_name__istartswith',
                     'prescription__doctor__last_name__istartswith',
                     'symptoms__istartswith', 'diagnosis__istartswith']
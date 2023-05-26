from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.core.validators import MinValueValidator
from .managers import UserManager

APPROVAL_CHOICES = (
    ('approved', 'Approved'),
    ('pending', 'Pending'),
    ('rejected', 'Rejected'),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
)

PAYEMENT_CHOICES = (
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Doctor(models.Model):
    specialization = models.CharField(max_length=255)
    location = models.OneToOneField(
        'Location', on_delete=models.CASCADE, related_name='doctor_id')
    charges = models.DecimalField(max_digits=8, decimal_places=2, 
                                  validators=[MinValueValidator(1)])
    approval_status = models.CharField(
        max_length=20, choices=APPROVAL_CHOICES, default='pending')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user.user_type = 'doctor'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email
    
    def phone_number(self):
        return self.user.phone_number

    def gender(self):
        self.user.gender

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'
        ordering = ['user__first_name', 'user__last_name']


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email
    
    def phone_number(self):
        return self.user.phone_number
    
    def gender(self):
        return self.user.gender

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['user__first_name', 'user__last_name']


class Location(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}"

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['city', 'state']


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    approval = models.CharField(
        max_length=20, choices=APPROVAL_CHOICES, default='pending')

    def __str__(self):
        return f"{self.patient} {self.doctor} {self.date} {self.time}"

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        constraints = [
            models.UniqueConstraint(
                fields=['patient', 'doctor', 'date', 'time'], name='unique_appointment'
            )
        ]
        ordering = ['date', 'time']


class Payment(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.CharField(
        max_length=20, choices=PAYEMENT_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.appointment} {self.amount}"

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['amount']


class Review(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} {self.doctor} {self.rating}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['rating']


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    prescription = models.TextField()

    def __str__(self):
        return f"{self.patient} {self.doctor} {self.date}"

    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = 'Prescriptions'
        ordering = ['date']


class MedicalRecord(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()

    def __str__(self):
        return f"{self.prescription}"

    class Meta:
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'

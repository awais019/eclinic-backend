from django.db import models


STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
)

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


class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    speicilization = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    location = models.ForeignKey(
        'Location', on_delete=models.CASCADE, related_name='doctor_id')
    charges = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active')
    approval_status = models.CharField(
        max_length=20, choices=APPROVAL_CHOICES, default='pending')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'


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


class Review(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.patient} {self.doctor} {self.rating}"

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


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


class MedicalRecord(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()

    def __str__(self):
        return f"{self.prescription}"

    class Meta:
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'

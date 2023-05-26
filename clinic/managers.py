from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name='XYZ', last_name='XYZ', phone_number='XYZ', gender='male',
                    password=None, is_admin=False, is_staff=False, is_active=True, user_type='admin'):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not first_name:
            raise ValueError("User must have a first name")
        if not last_name:
            raise ValueError("User must have a last name")
        if not phone_number:
            raise ValueError("User must have a phone number")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.set_password(password)  # change password to hash
        user.gender = gender
        user.is_superuser = is_admin
        user.is_staff = is_staff
        user.is_active = is_active
        user.user_type = user_type
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, gender, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            gender,
            password=password,
            is_staff=True,
            user_type='staff'
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
            user_type='admin'
        )
        return user
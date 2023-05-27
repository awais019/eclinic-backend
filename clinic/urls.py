from django.urls import path
from rest_framework_nested.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import index, UserProfileViewSet, DoctorRegisterViewSet, DoctorListViewSet, \
                DoctorRetrieveViewSet, PatientRegisterViewSet

router = SimpleRouter()
router.register('auth/users', UserProfileViewSet, basename='users')
router.register('doctors/register', DoctorRegisterViewSet, basename='doctors-register')
router.register('doctors', DoctorListViewSet, basename='doctors')
router.register('doctors', DoctorRetrieveViewSet, basename='doctors')

router.register('patients/register', PatientRegisterViewSet, basename='patients-register')

urlpatterns = [path('', index),
               path('auth/signin/', TokenObtainPairView.as_view()),
                path('auth/refresh/', TokenRefreshView.as_view())
               ] + router.urls

from django.urls import path
from rest_framework_nested.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import index, UserProfileViewSet,DoctorRegisterViewSet

router = SimpleRouter()
router.register('auth/users', UserProfileViewSet, basename='users')
router.register('doctors/register', DoctorRegisterViewSet, basename='doctors-register')

urlpatterns = [path('', index),
               path('auth/signin/', TokenObtainPairView.as_view()),
                path('auth/refresh/', TokenRefreshView.as_view())
               ] + router.urls

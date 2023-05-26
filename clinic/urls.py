from django.urls import path
from .views  import index
from rest_framework_nested.routers import SimpleRouter

from .views import DoctorRegisterViewSet

router = SimpleRouter()
router.register('doctors/register', DoctorRegisterViewSet, basename='doctors-register')

urlpatterns = [path('', index)] + router.urls

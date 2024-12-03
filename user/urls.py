from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserRegisterViewSet, UserLoginViewSet

router = DefaultRouter()
router.register('', UserRegisterViewSet, basename='register')
router.register('', UserLoginViewSet, basename='login')

urlpatterns = [
    path('', include(router.urls))
]

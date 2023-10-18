from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('own_secrets', UserSecrets, basename="own_secrets")
router.register('shared_secrets', SharedSecrets, basename="shared_secrets")

urlpatterns = [
    path("", include(router.urls)),
    path("create/", CreateSecret.as_view()),
    path("decrypt/", DecryptSecrets.as_view())
]

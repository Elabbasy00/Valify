
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include("users.urls")),
    path('secret/', include("secret.urls")),

    # path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")),)

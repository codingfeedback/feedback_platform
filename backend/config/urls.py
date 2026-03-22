from django.contrib import admin
from django.urls import include, path

from apps.api.router import router


urlpatterns = [
    path("", include("apps.demo.urls")),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]

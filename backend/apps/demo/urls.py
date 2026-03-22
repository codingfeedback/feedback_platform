from django.urls import path

from .views import AppPrototypeView, DemoIndexView


urlpatterns = [
    path("", AppPrototypeView.as_view(), name="app-prototype"),
    path("ops/", DemoIndexView.as_view(), name="demo-index"),
]

from django.urls import path

from .views import AppPrototypeView, DemoIndexView, LoginView


urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("app/", AppPrototypeView.as_view(), name="app-prototype"),
    path("ops/", DemoIndexView.as_view(), name="demo-index"),
]

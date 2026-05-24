from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "demo/login.html"


class AppPrototypeView(TemplateView):
    template_name = "demo/app.html"


class DemoIndexView(TemplateView):
    template_name = "demo/index.html"

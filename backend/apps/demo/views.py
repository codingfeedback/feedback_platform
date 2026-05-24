from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "demo/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["oauth_ready"] = {
            "google": bool(__import__("os").getenv("GOOGLE_OAUTH_CLIENT_ID")),
            "kakao": bool(__import__("os").getenv("KAKAO_OAUTH_CLIENT_ID")),
            "naver": bool(__import__("os").getenv("NAVER_OAUTH_CLIENT_ID")),
        }
        return context


class AppPrototypeView(TemplateView):
    template_name = "demo/app.html"


class DemoIndexView(TemplateView):
    template_name = "demo/index.html"

from hashlib import sha256
from pathlib import Path

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView


APP_ASSET_DIR = Path(__file__).resolve().parent / "static" / "demo"


def app_asset_version(name):
    return sha256((APP_ASSET_DIR / name).read_bytes()).hexdigest()[:12]


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


@method_decorator(never_cache, name="dispatch")
class AppPrototypeView(TemplateView):
    template_name = "demo/app.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["asset_versions"] = {
            "css": app_asset_version("app.css"),
            "js": app_asset_version("app.js"),
        }
        return context


class DemoIndexView(TemplateView):
    template_name = "demo/index.html"

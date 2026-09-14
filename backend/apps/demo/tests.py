from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.test import TestCase


class DemoPageTests(TestCase):
    def test_login_page_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google 설정 필요")
        self.assertContains(response, "KakaoTalk 설정 필요")
        self.assertContains(response, "Naver 설정 필요")

    def test_app_prototype_loads(self):
        response = self.client.get("/app/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feedback Loop")
        self.assertContains(response, "커뮤니티 샘플 채우기")
        self.assertContains(response, "현재 사용자")
        self.assertContains(response, 'id="myWorkList"')
        self.assertContains(response, 'id="workDetail"')
        self.assertContains(response, "demo/app.css")
        self.assertContains(response, "demo/app.js")

    def test_ops_page_loads(self):
        response = self.client.get("/ops/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Creative Feedback Platform")

    def test_app_asset_urls_change_when_files_change(self):
        with TemporaryDirectory() as directory:
            assets = Path(directory)
            (assets / "app.css").write_bytes(b"body { color: black; }")
            (assets / "app.js").write_bytes(b"const version = 1;")
            with patch("apps.demo.views.APP_ASSET_DIR", assets):
                first = self.client.get("/app/")
                repeated = self.client.get("/app/")
                (assets / "app.css").write_bytes(b"body { color: brown; }")
                updated = self.client.get("/app/")

        self.assertEqual(first.context["asset_versions"], repeated.context["asset_versions"])
        self.assertNotEqual(first.context["asset_versions"]["css"], updated.context["asset_versions"]["css"])
        self.assertEqual(first.context["asset_versions"]["js"], updated.context["asset_versions"]["js"])
        self.assertContains(updated, "app.css?v=" + updated.context["asset_versions"]["css"])
        self.assertContains(updated, "app.js?v=" + updated.context["asset_versions"]["js"])
        self.assertIn("no-store", updated.headers["Cache-Control"])

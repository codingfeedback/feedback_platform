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

    def test_ops_page_loads(self):
        response = self.client.get("/ops/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Creative Feedback Platform")

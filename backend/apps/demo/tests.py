from django.test import TestCase


class DemoPageTests(TestCase):
    def test_app_prototype_loads(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feedback Loop")

    def test_ops_page_loads(self):
        response = self.client.get("/ops/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Creative Feedback Platform")

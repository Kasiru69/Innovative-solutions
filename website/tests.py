from django.test import Client, TestCase


class HealthTests(TestCase):
    def test_health_returns_ok(self):
        response = Client().get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

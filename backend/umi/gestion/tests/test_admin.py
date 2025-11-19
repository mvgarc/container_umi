from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAdminDashboardTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser("admin", "admin@test.com", "password")
        self.client.force_login(self.user)

    def test_dashboard_loads_successfully(self):
        url = reverse("custom_admin:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard UMI")

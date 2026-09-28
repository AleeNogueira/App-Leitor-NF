from django.test import TestCase
from django.urls import reverse


class LocalLoginTests(TestCase):
	def test_upload_redirects_to_login_when_unauthenticated(self):
		response = self.client.get(reverse("upload_nota_fiscal"))

		self.assertRedirects(response, f"{reverse('login')}?next={reverse('upload_nota_fiscal')}")

	def test_admin_credentials_start_session(self):
		response = self.client.post(
			reverse("login"),
			{"username": "admin", "password": "admin"},
		)

		self.assertRedirects(response, reverse("upload_nota_fiscal"))
		self.assertTrue(self.client.session["local_user_authenticated"])

	def test_invalid_credentials_are_rejected(self):
		response = self.client.post(
			reverse("login"),
			{"username": "admin", "password": "wrong"},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Usuário ou senha inválidos.")

	def test_logout_clears_session(self):
		self.client.post(reverse("login"), {"username": "admin", "password": "admin"})

		response = self.client.post(reverse("logout"))

		self.assertRedirects(response, reverse("login"))
		self.assertNotIn("local_user_authenticated", self.client.session)

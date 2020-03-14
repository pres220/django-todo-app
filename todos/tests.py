from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class HomePageTest(SimpleTestCase):

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_homepage_reverse_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class SignUpPageTest(SimpleTestCase):

    def test_signup_status_code(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_reverse_url(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'signup.html')



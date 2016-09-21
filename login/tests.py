
from django.test import TestCase

# Create your tests here.

from django.test import Client

class LoginTest(TestCase):

    def test_authenticateUser(self):

        client = Client()
        response = self.client.post('/authenticate/', {'username': 'fred', 'email': 'secret', 'kaid': '12121', 'avatar_url':'asdafs'})
        self.assertEqual(response.content, 'True')


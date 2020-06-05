from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


class UnauthenticatedTestQuestionnaires(APITestCase):
    """Questionnaire Tests"""

    def test_get_questionnaires(self):
        """
        Unauthenticated users should not be able to access questionnaires via APIListView
        """

        url = reverse('make_questionnaire_app:questionnaire-list')
        response = self.client.get(url)

        print('')
        print('')
        print('make_questionnaire: test 1')
        print('Unauthenticated users should not be able to access questionnaires via APIListView')
        print(response.data)
        print('_________________')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTestQuestionnaires(APITestCase):
    """Questionnaire Tests"""

    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user = self.client.post('/auth/users/', data={'username': 'Test2', 'password': 'TestPassword2'})
        # obtain a json web token for the newly created user
        response = self.client.post('/auth/jwt/create/', data={'username': 'Test2', 'password': 'TestPassword2'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_header_for_token_verification(self):
        """
        https://stackoverflow.com/questions/47576635/django-rest-framework-jwt-unit-test
        Tests that users can access questionnaires with JWT tokens
        """

        verify_url = reverse('jwt-verify')
        credentials = {
            'token': self.token
        }
        resp = self.client.post(verify_url, credentials, format='json')

        print('')
        print('')
        print('make_questionnaire: test 2')
        print('Tests that users can access questionnaires with JWT tokens')
        print(resp.data)
        print('_________________')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

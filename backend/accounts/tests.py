from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


# test the user registration endpoint
class RegistrationTestCase(APITestCase):
    """Accaunts Registration Tests"""
    def test_registration(self):
        """
        Test the user registration endpoint
        """
        data = {"username": "Test1", "password": "TestPassword1", "email": "test1@test1.com"}
        response = self.client.post('/auth/users/', data)
        print('')
        print('')
        print('accounts: test 1')
        print('test the user registration endpoint')
        print(response.data)
        print('_________________')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# test case for the userprofile model
class userProfileTestCase(APITestCase):
    profile_list_url = reverse('accounts:accounts-list')
    profile_detail_url = reverse('accounts:accounts-detail', kwargs={'pk': 2})

    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user = self.client.post('/auth/users/', data={'username': 'Test2', 'password': 'TestPassword2'})
        # obtain a json web token for the newly created user
        response = self.client.post('/auth/jwt/create/', data={'username': 'Test2', 'password': 'TestPassword2'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # retrieve a list of all user profiles while the request user is authenticated
    def test_userprofile_list_authenticated(self):
        response = self.client.get(self.profile_list_url)
        print('')
        print('')
        print('accounts: test 2.1')
        print('retrieve a list of all user profiles while the request user is authenticated')
        print(response.data)
        print('_________________')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(self.profile_detail_url)
        print('')
        print('accounts: test 2.2')
        print('check to retrieve the profile details of the authenticated user')
        print(response.data)
        print('_________________')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile_data = {'description': 'I am a very famous game character', 'location': 'nintendo world',
                        'is_manager': 'true', }
        response = self.client.put(self.profile_detail_url, data=profile_data)
        print('')
        print('accounts: test 2.3')
        print('populate the user profile that was automatically created using the signals')
        print(response.data)
        print('_________________')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # retrieve a list of all user profiles while the request user is unauthenticated
    def test_userprofile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.profile_list_url)
        print('')
        print('')
        print('accounts: test 3')
        print('retrieve a list of all user profiles while the request user is unauthenticated')
        print(response.data)
        print('_________________')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

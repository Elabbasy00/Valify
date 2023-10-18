from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from business_logic.adapter.repository import UserRepository
from django.contrib import auth
from business_logic.services.services import AsymmetricEncrypt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

hardCodedUser = {
    "email": "ahmedelabbasy5@gmail.com",
    "username": "ahmed",
    "password": "010202020aA",
    "first_name": "Ahmed",
    "last_name": "Elabbasy"
}

userDetail = {
    "email": "ahmedelabbasy5@gmail.com",
    "username": "ahmed",
    "first_name": "Ahmed",
    "last_name": "Elabbasy"
}

FakeUser = {
    "email": "ahmedelabbasy@gmail.com",
    "username": "ahmed1",
    "password": "010202020"
}


class TestRegister(APITestCase):

    def test_register(self):
        request = self.client.post(
            "/user/register/", hardCodedUser, format='json')
        user = UserRepository.get_by_id(1)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, hardCodedUser.get("username"))
        loaded_key = AsymmetricEncrypt().load_private_key(
            request.json()['private_key'])
        self.assertTrue(isinstance(loaded_key, RSAPrivateKey))


class APIAuthTest(APITestCase):
    def setUp(self) -> None:
        UserRepository().create_user(hardCodedUser)
        self.auth_client = APIClient(enforce_csrf_checks=True)

    def test_happy_login(self):
        login_req = self.auth_client.post(
            '/user/login/', hardCodedUser, format='json', follow=True
        )
        user = auth.get_user(self.auth_client)  # get user from session
        self.assertEqual(user.is_authenticated, True)
        self.assertEqual(login_req.status_code, status.HTTP_200_OK)

    def test_error_login(self):
        login_req = self.auth_client.post(
            '/user/login/', FakeUser, format='json', follow=True
        )
        user = auth.get_user(self.auth_client)

        self.assertEqual(user.is_anonymous, True)
        self.assertEqual(login_req.status_code, status.HTTP_400_BAD_REQUEST)

    def test_happy_user_view(self):
        self.auth_client.post(
            '/user/login/', hardCodedUser, format='json', follow=True
        )
        detail_request = self.auth_client.get(
            '/user/detail/', format='json')
        self.assertEqual(detail_request.data, userDetail)
        self.assertEqual(detail_request.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        self.auth_client.post(
            '/user/login/', hardCodedUser, format='json', follow=True
        )
        detail_request = self.auth_client.get(
            '/user/detail/', format='json')

        self.assertEqual(detail_request.data, userDetail)

        self.auth_client.post('/user/logout/')

        detail_request1 = self.auth_client.get(
            '/user/detail/', format='json')

        self.assertEqual(detail_request1.status_code,
                         status.HTTP_403_FORBIDDEN)

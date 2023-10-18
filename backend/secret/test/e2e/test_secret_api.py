from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from business_logic.adapter.repository import SecretRepositorie
from business_logic.exceptions.exceptions import ValidationError, InvalidKey, NotFound, Errors

hardCodedUser = {
    "email": "ahmedelabbasy5@gmail.com",
    "username": "ahmed",
    "password": "010202020aA",
    "first_name": "Ahmed",
    "last_name": "Elabbasy"
}

hardCodedUser1 = {
    "email": "ahmedelabbasy1@gmail.com",
    "username": "ahmed1",
    "password": "010202020aA",
    "first_name": "Ahmed1",
    "last_name": "Elabbasy"
}
hardCodedUser2 = {
    "email": "ahmedelabbasy2@gmail.com",
    "username": "ahmed2",
    "password": "010202020aA",
    "first_name": "Ahmed2",
    "last_name": "Elabbasy"
}
secret = {
    "name": "Payment",
    "text": "This is my payment data",
    "recipients": [2, 3]
}

error_secret = {

}


class TestSecrets(APITestCase):
    def setUp(self):
        super(TestSecrets, self).setUp()
        self.auth_client = APIClient()

        request = self.auth_client.post(
            "/user/register/", hardCodedUser, format='json')
        user1 = self.auth_client.post(
            "/user/register/", hardCodedUser1, format='json')
        self.auth_client.post(
            "/user/register/", hardCodedUser2, format='json')

        self.private_key = request.json()['private_key'].encode("utf-8")
        self.shared_with_key = user1.json()['private_key'].encode("utf-8")

        self.auth_client.post(
            '/user/login/', hardCodedUser, format='json', follow=True
        )

    def test_atomic_not_save(self):
        not_exisit_recipient = {
            "name": "Payment",
            "text": "This is my payment data",
            "recipients": [111]
        }
        self.auth_client.post(
            '/secret/create/', not_exisit_recipient, format='json', follow=True
        )

        user_secrets = SecretRepositorie.get_user_secret(1)
        self.assertEqual(user_secrets.count(), 0)

    def test_happy_create_secret(self):
        request = self.auth_client.post(
            '/secret/create/', secret, format='json', follow=True
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        created_secret = SecretRepositorie.get_user_secret(1)
        self.assertEqual(created_secret.count(), 1)
        shared_secret1 = SecretRepositorie.get_shared_secret(2)
        shared_secret2 = SecretRepositorie.get_shared_secret(3)
        self.assertEqual(shared_secret1.count(), 1)
        self.assertEqual(shared_secret2.count(), 1)

    def test_invalid_data_create_secret(self):
        request = self.auth_client.post(
            '/secret/create/', error_secret, format='json', follow=True
        )
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(request.data['error'], Errors.missing_data.value.format(
            "name, text, recipient"))

    def test_decrypt_own_secret(self):
        request = self.auth_client.post(
            '/secret/create/', secret, format='json', follow=True
        )
        secret_share_data = {
            "secret_id": 1,
            "private_key": self.private_key
        }
        request = self.auth_client.post(
            '/secret/decrypt/', secret_share_data, format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['text'], secret["text"])

    def test_decrypt_shared_secret(self):
        request = self.auth_client.post(
            '/secret/create/', secret, format='json', follow=True
        )
        secret_share_data = {
            "secret_id": 1,
            "private_key": self.shared_with_key
        }
        self.client.logout()  # remove cookies

        self.auth_client.post(
            '/user/login/', hardCodedUser1, format='json', follow=True
        )
        request = self.auth_client.post(
            '/secret/decrypt/', secret_share_data, format='json'
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(request.data['text'], secret["text"])

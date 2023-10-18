from django.test import TestCase
from business_logic.adapter.repository import UserRepository


hardCodedUser = {
    "username": "ahmed",
    "email": "ahmedelabbasy5@gmail.com",
    "password": "010202020aA"
}


class UserTestCase(TestCase):
    def setUp(self) -> None:
        self.repository = UserRepository()
        self.repository.create_user(hardCodedUser)

    def test_get_user(self):
        user = UserRepository().get_by_id(1)
        self.assertEqual(user.username, hardCodedUser.get('username'))

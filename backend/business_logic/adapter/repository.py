from django.contrib.auth import get_user_model
from secret.models import Secret, RecipientKeys
from business_logic.exceptions.exceptions import NotFound
User = get_user_model()


class UserRepository:
    @staticmethod
    def get_by_id(id: int) -> User:
        user = User.objects.get(id=id)
        return user

    @staticmethod
    def create_user(data) -> User:
        new_user = User.objects.create_user(**data)
        return new_user

    @staticmethod
    def get_filterd_list(user_list):
        return User.objects.filter(id__in=user_list)


class SecretRepositorie():

    @staticmethod
    def create_secret(user, name, key, cipher_text) -> Secret:
        return Secret.objects.create(
            user=user, name=name, key=key, cipher_text=cipher_text)

    @staticmethod
    def get_single_secret(secret_id):
        try:
            return Secret.objects.get(id=secret_id)
        except Secret.DoesNotExist:
            raise NotFound(secret_id)

    @staticmethod
    def get_user_secret(user_id):
        user_secret_list = Secret.objects.filter(user=user_id).prefetch_related(
            "shared_with__user")
        return user_secret_list

    @staticmethod
    def create_secret_recipients(recipient_list):
        return RecipientKeys.objects.bulk_create(recipient_list)

    @staticmethod
    def generate_single_recipients(user, secret, key):
        return RecipientKeys(user=user, secret=secret, key=key)

    @staticmethod
    def get_shared_secret(user_id):
        return RecipientKeys.objects.filter(user=user_id).select_related('secret', "user")

    @staticmethod
    def get_single_shared_secret(user_id, secret_id):
        try:
            return RecipientKeys.objects.get(user=user_id, secret_id=secret_id)
        except RecipientKeys.DoesNotExist:
            raise NotFound(secret_id)

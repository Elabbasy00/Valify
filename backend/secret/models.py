from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Secret
# ------
# User -> ForginKey
# Name -> Secret Name
# Key -> The PrivateKey CharField
# chiper_text -> Encrypted text 10 ** 5

# RecipientKEy
# -----
# user -> Participate with him
# secret -> shared secret
# key -> encrypted key for particular user


class Secret(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_for")
    name = models.CharField(_("Secret Title"), max_length=200)
    # Saves us from messing with decoded and encoding issue
    # owner Symmetric key encrypted with asymmetric
    key = models.BinaryField(_("Symmetric Key"))
    cipher_text = models.TextField(_("Encrypted Text"), max_length=10 ** 5)

    def __str__(self):
        return self.name


class RecipientKeys(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="shared_with_user")
    secret = models.ForeignKey(
        Secret, on_delete=models.CASCADE, related_name="shared_with")
    key = models.BinaryField(_("Symmetric Key"))

    def __str__(self):
        return self.secret.name


# class Shared_Secret(models.Model):
#     recipient = models.ManyToManyField(RecipientKeys)
#     secret = models.ForeignKey(Secret, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.secret.name

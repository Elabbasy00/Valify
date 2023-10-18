from business_logic.services.services import AsymmetricEncrypt, SymmetricEncrypt, create_secret, create_recipient
from django.test import TestCase
from cryptography.hazmat.primitives.asymmetric import rsa
from business_logic.exceptions.exceptions import InvalidKey, Errors
from business_logic.adapter.repository import UserRepository


class TestEncrypt(TestCase):
    def test_happy_symmetric(self):
        symmetric = SymmetricEncrypt()
        message = "Im a secret message"
        key, encrypted_message = symmetric.symmetric_encrypt(message)
        decrypted_message = symmetric.symmetric_decrypt(key, encrypted_message)
        self.assertEqual(message, decrypted_message)

    def test_error_symmetric(self):
        symmetric = SymmetricEncrypt()
        guess_password = bytes.fromhex(
            "785754746c6136366d4f467431395543336c46444c71692d3249792d5a365374386665566f64726f4639303d")
        message = "Im a secret message"
        _, encrypted_message = symmetric.symmetric_encrypt(message)

        with self.assertRaisesMessage(InvalidKey, Errors.invalid_key.value.format("", "symmetric")) as e:
            symmetric.symmetric_decrypt(
                guess_password, encrypted_message)

    def test_generate_private_key(self):
        asymmetric = AsymmetricEncrypt()
        private, public = asymmetric.generate_key_pair()
        self.assertTrue(isinstance(private, rsa.RSAPrivateKey))
        self.assertTrue(isinstance(public, rsa.RSAPublicKey))
        self.assertEqual(private.key_size, 2048)

    def test_convert_private_key(self):
        asymmetric = AsymmetricEncrypt()
        private, _ = asymmetric.generate_key_pair()
        key_bytes = asymmetric.private_bytes(private)
        self.assertEqual(key_bytes.splitlines()[
                         0], b"-----BEGIN PRIVATE KEY-----")

    def test_convert_public_key(self):
        asymmetric = AsymmetricEncrypt()
        _, public = asymmetric.generate_key_pair()
        key_bytes = asymmetric.public_bytes(public)
        self.assertEqual(key_bytes.splitlines()[
                         0], b"-----BEGIN PUBLIC KEY-----")

    def test_load_private_key(self):
        asymmetric = AsymmetricEncrypt()
        private, _ = asymmetric.generate_key_pair()
        key_bytes = asymmetric.private_bytes(private).decode()
        loaded_key = asymmetric.load_private_key(key_bytes)
        self.assertTrue(isinstance(loaded_key, rsa.RSAPrivateKey))

    def test_load_public_key(self):
        asymmetric = AsymmetricEncrypt()
        _, public = asymmetric.generate_key_pair()
        key_bytes = asymmetric.public_bytes(public).decode()
        loaded_key = asymmetric.load_public_key(key_bytes)
        self.assertTrue(isinstance(loaded_key, rsa.RSAPublicKey))

    def test_happy_asymmetric(self):
        asymmetric = AsymmetricEncrypt()
        message = b"Im a secret message"
        private, public = asymmetric.generate_key_pair()
        encrypted_message = asymmetric.encrypt(message, public)
        decrypted_message = asymmetric.decrypt(private, encrypted_message)

        self.assertEqual(decrypted_message, message.decode())

    def test_error_asymmetric(self):
        asymmetric = AsymmetricEncrypt()
        message = b"Im a secret message"
        _, public = asymmetric.generate_key_pair()
        privateFake, _ = asymmetric.generate_key_pair()
        encrypted_message = asymmetric.encrypt(message, public)
        with self.assertRaisesMessage(InvalidKey, Errors.invalid_key.value.format("", "private_key")):
            asymmetric.decrypt(privateFake, encrypted_message)

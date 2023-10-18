from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.fernet import Fernet, InvalidToken
from business_logic.adapter.repository import SecretRepositorie, UserRepository
# from django.db import transaction
from business_logic.exceptions.exceptions import NotFound, InvalidKey
# import base64


# def encode_b64(string):
#     return base64.b64encode(string).decode("utf-8")


# def decode_b64(string):
#     return base64.b64decode(string.encode("utf-8"))


class SymmetricEncrypt():
    @staticmethod
    def symmetric_encrypt(message):
        '''
            symmetric encrypt the givin message
            return key , encryoted message
        '''
        key = Fernet.generate_key()
        cipher = Fernet(key)
        message_encrypted = cipher.encrypt(message.encode())
        return key, message_encrypted

    @staticmethod
    def symmetric_decrypt(key, message_encrypted):
        '''
            symmetric decrypt givin message with key pair
            return decoded text 
            @raise -> InvaldToken the password not valid
        '''
        cipher = Fernet(key)
        try:
            return cipher.decrypt(message_encrypted).decode()
        except InvalidToken:
            raise InvalidKey("", "symmetric")


class AsymmetricEncrypt():

    @staticmethod
    def generate_key_pair():
        '''
            generate Asymmetric Keys
        '''
        private_key = rsa.generate_private_key(
            key_size=2048,  # Avoiding vulnerabilities
            public_exponent=65537  # mathematical property
        )
        public_key = private_key.public_key()
        return private_key, public_key

    @staticmethod
    def private_bytes(privateKey):
        '''
            Convert Private Key to bytes
            Easy to store and return
        '''
        return privateKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            # encryption_algorithm=serialization.BestAvailableEncryption(b'mypassword')
            encryption_algorithm=serialization.NoEncryption()

        )

    @staticmethod
    def public_bytes(publicKey):
        '''
            Convert public Key to bytes
            Easy to store and return
        '''
        return publicKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    @staticmethod
    def load_private_key(key_bytes):
        '''
            revcive plain bytes text ( User Input )
            convert bytes key to RSAPrivateKey instance

            raise invalid key
        '''
        try:
            return load_pem_private_key(key_bytes.encode("utf-8"), password=None)
        except Exception:
            raise InvalidKey("", "private")

    @staticmethod
    def load_public_key(key_bytes):
        '''
            revcive plain bytes text ( DB Saved )
            convert bytes key to RSAPublicKey instance
        '''
        try:
            public_key = load_pem_public_key(key_bytes.encode("utf-8"))
            return public_key
        except Exception as e:
            raise InvalidKey("", "public")

    @staticmethod
    def encrypt(message, public_key):
        '''
            encrypt givin message with public key
            usually stored with user in DB
        '''
        try:
            encrypted_key = public_key.encrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return encrypted_key
        except Exception as e:
            raise InvalidKey("", "public_key")

    @staticmethod
    def decrypt(privateKey, cipher_text):
        '''
            decrypt message using user givin key

            @return decoded message
            @raise ValueError 
        '''
        try:

            plaintext = privateKey.decrypt(
                cipher_text,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            return plaintext.decode()
        except Exception as e:
            raise InvalidKey("", "private_key")


def create_secret(user, clean_data):
    '''
        args: user -> User Object
        Clean data -> text to encrypt, secret name, recipint
        ---
        check for user public_key and raise invalid key if not exist
        encrypt the text with symmetric
        then encrypt the symmetric key with asymmmetric
        return created secret and symmetric key for recipints 
    '''
    if not user.public_key:
        raise InvalidKey(user.username, "public")
    public_key = AsymmetricEncrypt.load_public_key(user.public_key)
    symmetric_key, encrypted_message = SymmetricEncrypt.symmetric_encrypt(
        clean_data.get("text"))
    asymmetric_key = AsymmetricEncrypt.encrypt(symmetric_key, public_key)

    secret = SecretRepositorie.create_secret(
        user, clean_data.get("name"), asymmetric_key,  encrypted_message.decode("utf-8"))
    return secret, symmetric_key


def create_recipient(recipient_list, secret, symmetric_key):
    '''
        args: recipient_list -> list conain user id to share secret with
              secret -> secret obj for relation
              symmetric_key -> reviced from create_secret()
        -----
        check for recipients if exisit
        loop throw them and check for public key invalid key will be rasie
        prevent owner to add to the shared with
        load the public key form db
        encrypt with symmetric and append the list for bulk create
    '''
    obj_list = []
    recipients = UserRepository.get_filterd_list(recipient_list)
    if recipients.exists():
        for user in recipients:
            if not user.public_key:
                raise InvalidKey(user.username, "public")

            if user == secret.user:
                continue

            public_key = AsymmetricEncrypt.load_public_key(
                user.public_key)

            asymmmetric_key = AsymmetricEncrypt.encrypt(
                symmetric_key, public_key)

            obj_list.append(SecretRepositorie.generate_single_recipients(
                user=user, secret=secret, key=asymmmetric_key))
        return SecretRepositorie.create_secret_recipients(obj_list)
    raise NotFound("Recipients")


def decrypt_secrets(data, obj):
    '''
        args: data -> cipher_text and private key
        obj: secret obj for owner and recipintKey for shared with
        ---
        check if its shared or owner
        load the private key
        decrypt the symmatric key
        return decrypted text
    '''
    if hasattr(obj, "cipher_text"):
        cipher_text = obj.cipher_text
    else:
        cipher_text = obj.secret.cipher_text

    private_key = AsymmetricEncrypt.load_private_key(
        data.get("private_key"))

    symmetric_key = AsymmetricEncrypt.decrypt(
        private_key, obj.key)

    return SymmetricEncrypt.symmetric_decrypt(symmetric_key, cipher_text)


# class CreateSecretUOW():
#     def __init__(self) -> None:
#         self.secret = None
#         self.recipient = []
#         self.symmetric = SymmetricEncrypt()
#         self.asymmetric = AsymmetricEncrypt()
#         self.symmetric_key = None

#     def __enter__(self):
#         transaction.set_autocommit(False)
#         return self

#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         if exc_type:
#             self.rollback()
#         transaction.set_autocommit(True)

#     def commit(self):
#         return SecretRepositorie.create_secret_recipients(
#             self.recipient)

#     def rollback(self):
#         transaction.rollback()

#     def create_secret(self, user, clean_data):

#         if not user.public_key:
#             raise InvalidKey(user.username, "public")

#         self.symmetric_key, encrypted_message = self.symmetric.symmetric_encrypt(
#             message=clean_data.get("text"))

#         public_key = self.asymmetric.load_public_key(
#             user.public_key)

#         asymmetric_key = self.asymmetric.encrypt(
#             self.symmetric_key, public_key)

#         self.secret = SecretRepositorie.create_secret(
#             user, name=clean_data.get('name'), key=asymmetric_key, cipher_text=encrypted_message.decode('utf8'))

#         return self.secret

#     def create_recipient(self, recipient_list):
#         recipients = UserRepository.get_filterd_list(recipient_list)

#         if recipients.exists():
#             for user in recipients:
#                 if not user.public_key:
#                     raise InvalidKey(user.username, "public")

#                 public_key = self.asymmetric.load_public_key(
#                     user.public_key)

#                 asymmmetric_key = self.asymmetric.encrypt(
#                     self.symmetric_key, public_key)

#                 self.recipient.append(SecretRepositorie.generate_single_recipients(
#                     user=user, secret=self.secret, key=asymmmetric_key))
#             return self.recipient
#         raise NotFound("Recipients")

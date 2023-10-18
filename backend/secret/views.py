from rest_framework.views import APIView
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from business_logic.services.services import create_recipient, create_secret, decrypt_secrets
from business_logic.adapter.repository import SecretRepositorie
from .serializers import RecipientKeysSerializer, SecretSerializer
from business_logic.exceptions.validation import check_secret_requirements, check_decrypt_requirements
from business_logic.exceptions.exceptions import ValidationError, NotFound, InvalidKey
from django.db import transaction
from rest_framework.authentication import SessionAuthentication


class UserSecrets(viewsets.ModelViewSet):
    serializer_class = SecretSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SecretRepositorie.get_user_secret(self.request.user.id)


class SharedSecrets(viewsets.ModelViewSet):
    serializer_class = RecipientKeysSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SecretRepositorie.get_shared_secret(self.request.user.id)


class CreateSecret(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (SessionAuthentication,)
    # serializer_class = SecretSerializer

    def post(self, request, format=None):
        try:
            data = check_secret_requirements(request.data)
            user = request.user

            # prevent saving any thing on error cuz we can't re ask
            # the user for private key to re append recipient
            with transaction.atomic():
                secret, symmetric_key = create_secret(user, data)
                # prevent duplication
                unique_recipint = set(data.get("recipients"))
                recipint = create_recipient(
                    unique_recipint, secret, symmetric_key)

                serializer = SecretSerializer(secret)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:

            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        except NotFound as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        except InvalidKey as e:
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"Error Ocured While create Secret {}".format(e)}, status=status.HTTP_400_BAD_REQUEST)


class DecryptSecrets(APIView):
    def post(self, request, format=None):
        try:
            data = check_decrypt_requirements(request.data)
            user = request.user

            secret = SecretRepositorie.get_single_secret(data.get("secret_id"))
            if secret.user != user:  # check if it's the owner? no?
                secret = SecretRepositorie.get_single_shared_secret(  # check if shared with? will raise not found
                    user.id, data.get("secret_id"))

            plain_text = decrypt_secrets(data, secret)
            return Response({"text": plain_text}, status=status.HTTP_200_OK)

        except ValidationError as e:
            print(e)
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        except InvalidKey as e:
            print(e)
            return Response({"error": e.message}, status=status.HTTP_400_BAD_REQUEST)

        except NotFound as e:
            print(e)
            return Response({"error": e.message}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            return Response({"Error Ocured While Decrypting the data {}".format(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from django.contrib.auth import get_user_model
from business_logic.adapter.repository import UserRepository
from business_logic.services.services import AsymmetricEncrypt
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        '''
            Custom Create Method to user Our Repo create_user()
            while password is required
            then create a certificate
            return user instance and private key 
        '''
        private, public = AsymmetricEncrypt.generate_key_pair()
        private_bytes = AsymmetricEncrypt.private_bytes(private)
        public_bytes = AsymmetricEncrypt.public_bytes(public)
        validated_data['public_key'] = public_bytes.decode('utf8')
        user_obj = UserRepository().create_user(validated_data)
        # TODO: send the privateKey to user email ?
        return user_obj, private_bytes.decode('utf8')


class UserLoginSerializer(serializers.Serializer):
    '''
    Validation Proccess
    '''
    email = serializers.EmailField()
    password = serializers.CharField()

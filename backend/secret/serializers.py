from rest_framework import serializers
from .models import Secret, RecipientKeys


class ShareWithSerializer(serializers.ModelSerializer):
    '''
        return secret information for shared secret
        view json using related fields
    '''
    username = serializers.PrimaryKeyRelatedField(
        read_only=True, source="user.username")

    class Meta:
        model = RecipientKeys
        fields = ("username",)


class SecretSerializer(serializers.ModelSerializer):
    shared_with = ShareWithSerializer(many=True, read_only=True)

    class Meta:
        model = Secret
        fields = "__all__"


class SecretSharedDetail(serializers.ModelSerializer):
    '''
        main secret fields to appers in json response
        for shared secret
    '''
    class Meta:
        model = Secret
        fields = ("id", "name", "user")


class RecipientKeysSerializer(serializers.ModelSerializer):
    secret = SecretSharedDetail(read_only=True)

    class Meta:
        model = RecipientKeys
        fields = "__all__"

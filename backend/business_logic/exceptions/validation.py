from business_logic.exceptions.exceptions import ValidationError


def check_secret_requirements(data):

    if data:
        if not data.get('name'):
            raise ValidationError("name")
        if not data.get('text'):
            raise ValidationError("text")
        if not data.get('recipients') or type(data.get('recipients')) != list or len(data.get('recipients')) < 1:
            raise ValidationError("recipients")

        return data
    raise ValidationError("name, text, recipient")


def check_decrypt_requirements(data):
    if data:
        if not data.get('secret_id'):
            raise ValidationError("Secret ID")
        if not data.get('private_key'):
            raise ValidationError("Private Key")
        return data

    raise ValidationError("Private Key, Secret ID")

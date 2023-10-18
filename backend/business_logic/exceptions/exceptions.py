from enum import Enum
from rest_framework.exceptions import APIException


class Errors(Enum):
    not_found = "{} not found"
    doesnt_exist = "{} doesn't exist"
    missing_data = "{} must be set"
    invalid_key = "{} has an invalid {} Key"


class NotFound(Exception):
    """
    Exception raised for any dose not exisit object errors .
    """

    def __init__(self, not_founded_obj):
        self.message = Errors.doesnt_exist.value.format(not_founded_obj)
        super().__init__(self.message)


class ValidationError(Exception):
    """
    Exception raised for any missing data .
    """

    def __init__(self, invalid_obj):
        self.message = Errors.missing_data.value.format(invalid_obj)
        super().__init__(self.message)


class InvalidKey(Exception):
    """
    Exception raised for any invalid private, public key .
    """

    def __init__(self, user, key):
        self.message = Errors.invalid_key.value.format(user, key)
        super().__init__(self.message)


# class ServiceUnavailable(APIException):
#     status_code = 503
#     default_detail = 'Service temporarily unavailable, try again later.'
#     default_code = 'service_unavailable'

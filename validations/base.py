"""
Validation module for all entities.
"""

from typing import Any
from flask_smorest import abort
from services.numverify import NumVerify


class BaseValidation:
    """
    Base validation class providing common validation utilities.

    This class serves as a foundation for entity-specific validators,
    offering reusable methods for payload validation, type checking,
    and standardized error responses.
    """

    @staticmethod
    def abort_with_error(status_code: int, message: str, field: str = 'json') -> None:
        """
        Abort with a status code error.

        Args:
            status_code (int): The HTTP status code.
            message (str): The error message to display.
            field (str): The field name for error categorization. Defaults to 'json'.

        Raises:
            HTTPException: Always raises with the specified status code.
        """
        abort(status_code, errors={'json': {field: [message]}})

    @staticmethod
    def validate_positive_int(value: Any, name: str = 'id') -> None:
        """
        Validate that a value is a positive integer.

        Args:
            value (Any): The value to validate.
            name (str): The field name for error messages. Defaults to 'id'.

        Raises:
            HTTPException: If value is not a positive integer (400).
        """
        if not isinstance(value, int) or value <= 0:
            BaseValidation.abort_with_error(400, f'Invalid {name}.', name)

    @staticmethod
    def abort_email_conflict() -> None:
        """
        Abort with a 409 Conflict error for duplicate email.

        Raises:
            HTTPException: Always raises a 409 Conflict.
        """
        BaseValidation.abort_with_error(
            409, 'Email already registered.', 'email')

    @staticmethod
    def abort_phone_number_conflict() -> None:
        """
        Abort with a 409 Conflict error for duplicate phone number.

        Raises:
            HTTPException: Always raises a 409 Conflict.
        """
        BaseValidation.abort_with_error(
            409, 'Phone number already registered.', 'phone_number')

    @staticmethod
    def abort_invalid_phone_number() -> None:
        """
        Abort with a 400 Bad Request error for invalid phone number.

        Raises:
            HTTPException: Always raises a 400 Bad Request.
        """
        BaseValidation.abort_with_error(
            400, 'The provided phone number is invalid.', 'phone_number')

    @staticmethod
    def validate_update_payload(payload: dict, allowed_update_fields: dict[str, type]) -> dict:
        """
        Validate and clean the update payload.

        Args:
            payload (dict): Raw update data.
            allowed_update_fields (dict[str, type]): Mapping of field names to their expected types.

        Returns:
            dict: Cleaned dictionary with only valid fields.

        Raises:
            BadRequest: If payload contains invalid types or no valid fields.
        """
        cleaned = {}

        for field, expected_type in allowed_update_fields.items():
            value = payload.get(field)
            if value is None:
                continue
            if not isinstance(value, expected_type):
                BaseValidation.abort_with_error(
                    400, f"Field '{field}' must be of type {expected_type.__name__}.", field)
            cleaned[field] = value

        if not cleaned:
            BaseValidation.abort_with_error(
                400, 'No valid fields to update.')

        return cleaned

    @staticmethod
    def _phone_number_pre_validation(phone_number: str) -> None:
        if not isinstance(phone_number, str):
            BaseValidation.abort_invalid_phone_number()

        allowed = phone_number.startswith("+55") and phone_number[3:].isdigit()
        only_digits = phone_number.isdigit()

        if not (allowed or only_digits):
            BaseValidation.abort_invalid_phone_number()

        digits = phone_number.lstrip("+")
        if digits.startswith("55"):
            digits = digits[2:]

        if len(digits) != 11:
            BaseValidation.abort_invalid_phone_number()

        ddd = digits[:2]
        if not (ddd.isdigit() and 10 <= int(ddd) <= 99):
            BaseValidation.abort_invalid_phone_number()

    @staticmethod
    def validate_brazilian_phone_number(phone_number: str) -> None:
        """
        Validate a Brazilian mobile phone number using the NumVerify API.

        This method performs pre-validation on the input format, sends the number
        for external API verification, and applies domain rules to ensure that:

            - The number is valid
            - The number belongs to Brazil (country_code = 'BR')
            - The line type is a mobile phone

        If any of these conditions fail, a validation error is raised through
        `BaseValidation.abort_invalid_phone_number()`.

        Args:
            phone_number (str): The phone number to validate.

        Raises:
            HTTPError: If the external API request fails.
            ValueError: If `phone_number` is malformed according to base validation rules.
            CustomValidationError: Triggered when the number does not meet requirements.
        """

        BaseValidation._phone_number_pre_validation(phone_number)

        response = NumVerify.validate_phone_number(phone_number)

        if not (
            response.get('valid') is True
            and response.get('country_code') == 'BR'
            and response.get('line_type') == 'mobile'
        ):
            BaseValidation.abort_invalid_phone_number()

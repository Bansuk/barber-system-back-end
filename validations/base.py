"""
Validation module for all entities.
"""

from typing import Any
from flask_smorest import abort


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

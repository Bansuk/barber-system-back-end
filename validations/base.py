"""Validation module for all entities."""

from typing import Any
from flask_smorest import abort
from werkzeug.exceptions import BadRequest


class BaseValidation:
    """
    Base validation class providing common validation utilities.

    This class serves as a foundation for entity-specific validators,
    offering reusable methods for payload validation, type checking,
    and standardized error responses.
    """

    @staticmethod
    def _abort_bad_request(message: str, field: str = 'json') -> None:
        """
        Abort with a 400 Bad Request error.

        Args:
            message: The error message to display.
            field: The field name for error categorization. Defaults to 'json'.

        Raises:
            HTTPException: Always raises a 400 Bad Request.
        """
        abort(400, errors={field: [message]})

    @staticmethod
    def validate_positive_int(value: Any, name: str = 'id') -> None:
        """
        Validate that a value is a positive integer.

        Args:
            value: The value to validate.
            name: The field name for error messages. Defaults to 'id'.

        Raises:
            HTTPException: If value is not a positive integer (400 Bad Request).
        """
        if not isinstance(value, int) or value <= 0:
            BaseValidation._abort_bad_request(f'Invalid {name}.')

    @staticmethod
    def abort_email_conflict() -> None:
        """
        Abort with a 409 Conflict error for duplicate email.

        Raises:
            HTTPException: Always raises a 409 Conflict.
        """
        abort(409, errors={'json': {'email': ['Email already registered.']}})

    @staticmethod
    def validate_update_payload(payload: dict, allowed_update_fields: dict[str, type]) -> dict:
        """
        Validate and clean the update payload.

        Args:
            payload: Raw update data.
            allowed_update_fields: Mapping of field names to their expected types.

        Returns:
            Cleaned dictionary with only valid fields.

        Raises:
            BadRequest: If payload contains invalid types or no valid fields.
        """
        cleaned = {}

        print(payload)

        for field, expected_type in allowed_update_fields.items():
            value = payload.get(field)
            if value is None:
                continue
            if not isinstance(value, expected_type):
                raise BadRequest(
                    description=f"Field '{field}' must be of type {expected_type.__name__}."
                )
            cleaned[field] = value

        if not cleaned:
            raise BadRequest(description='No valid fields to update.')

        return cleaned

"""
Validation module for Customer entities.
"""

from typing import Optional
from flask_smorest import abort
from werkzeug.exceptions import BadRequest
from repositories.customer_repository import search_customer_by_email


class CustomerValidation:
    """
    Validation class for Customer entities.
    """

    @staticmethod
    def _find_customer_by_email(email: str) -> Optional[str]:
        """
        Searches for the given email in the Customer database.

        Args:
            email (str): The email to check.

        Returns:
            Optional[str]: The email found or None.
        """

        return search_customer_by_email(email)

    @staticmethod
    def _validate_update_payload(payload: dict) -> dict:
        allowed = {'name': str, 'email': str}
        cleaned = {}

        for k, v in payload.items():
            if k not in allowed:
                continue
            if v is None:
                continue
            if not isinstance(v, allowed[k]):
                raise BadRequest(
                    description=f"Field '{k}' must be of type {allowed[k].__name__}.")

            cleaned[k] = v

        if not cleaned:
            raise BadRequest(description='No valid fields to update.')
        if 'email' in cleaned:
            CustomerValidation.validate_customer(cleaned['email'])

        return cleaned

    @staticmethod
    def validate_customer(email: str) -> None:
        """
        Validates customer.

        Args:
            email (str): The customer's email.

        Raises:
            HTTPException: If any validation fails.
        """

        if CustomerValidation._find_customer_by_email(email) is not None:
            abort(409, errors={
                'json': {
                    'email': ['Email already registered.']
                }
            })

    @staticmethod
    def validate_customer_update(fields: dict, current_customer_id: int = None) -> dict:
        """
        Validate update payload and check uniqueness constraints.

        Args:
            fields (dict): Raw update payload
            current_customer_id (int, optional): Id of the customer being updated.
                If provided, an existing record with the same email but the same id
                will not be considered a conflict.

        Returns:
            dict: Cleaned fields ready to apply.

        Raises:
            BadRequest: For invalid payloads.
            HTTPException: For uniqueness conflicts.
        """
        cleaned = CustomerValidation._validate_update_payload(fields)

        if 'email' in cleaned:
            existing = CustomerValidation._find_customer_by_email(
                cleaned['email'])
            if existing is not None:
                if current_customer_id is None or \
                        getattr(existing, 'id', None) != current_customer_id:
                    abort(409, errors={
                          'json': {'email': ['Email already registered.']}})

        return cleaned

"""
Validation module for Customer entities.
"""

from typing import Optional, TYPE_CHECKING
from validations.base import BaseValidation
from repositories.customer_repository import search_customer_by_email, \
    search_customer_by_phone_number

if TYPE_CHECKING:
    from ..database.models.customer import Customer

ALLOWED_UPDATE_FIELDS = {'name': str, 'email': str, 'phone_number': str}


class CustomerValidation:
    """
    Validation class for Customer entities.
    """

    @staticmethod
    def _find_customer_by_email(email: str) -> Optional['Customer']:
        """
        Searches for the given email in the Customer database.

        Args:
            email (str): The email to search for.

        Returns:
            Optional[Customer]: The customer object if found, otherwise None.
        """

        return search_customer_by_email(email)

    @staticmethod
    def _find_customer_by_phone_number(phone_number: str) -> Optional['Customer']:
        """
        Searches for the given phone number in the Customer database.

        Args:
            phone_number (str): The phone number to search for.

        Returns:
            Optional[Customer]: The customer object if found, otherwise None.
        """

        return search_customer_by_phone_number(phone_number)

    @staticmethod
    def validate_customer(email: str, phone_number: str) -> None:
        """
        Validates customer.

        Args:
            email (str): The customer's email.

        Raises:
            HTTPException: If any validation fails.
        """

        if CustomerValidation._find_customer_by_email(email) is not None:
            BaseValidation.abort_email_conflict()

        if CustomerValidation._find_customer_by_phone_number(phone_number) is not None:
            BaseValidation.abort_phone_number_conflict()

        BaseValidation.validate_brazilian_phone_number(phone_number)

    @staticmethod
    def validate_customer_update(
        fields: dict,
        current_customer_id: Optional[int] = None
    ) -> dict:
        """
        Validate update payload and check uniqueness constraints.

        Args:
            fields (dict): Raw update payload.
            current_customer_id (Optional[int]): ID of the customer being updated. If provided,
                allows the same email if it belongs to this customer.

        Returns:
            dict: Cleaned fields ready to apply.

        Raises:
            HTTPException: For uniqueness conflicts (409).
        """
        cleaned = BaseValidation.validate_update_payload(
            fields, allowed_update_fields=ALLOWED_UPDATE_FIELDS)

        if 'email' not in cleaned:
            return cleaned

        existing = CustomerValidation._find_customer_by_email(cleaned['email'])
        is_conflict = (
            existing is not None
            and (current_customer_id is None or
                 getattr(existing, 'id', None) != current_customer_id))

        if is_conflict:
            BaseValidation.abort_email_conflict()

        return cleaned

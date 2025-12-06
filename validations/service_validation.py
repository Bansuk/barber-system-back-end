"""
Validation module for Service entities.
"""

from typing import Optional, TYPE_CHECKING
from repositories.service_repository import get_service_by_name
from validations.base import BaseValidation

if TYPE_CHECKING:
    from ..database.models.service import Service

MAX_SERVICE_PRICE = 10000
MIN_SERVICE_PRICE = 2500
ALLOWED_STATUS_VALUES = ['available', 'unavailable']

ALLOWED_UPDATE_FIELDS = {'name': str, 'price': int, 'status': str}


class ServiceValidation:
    """
    Validation class for Service entities.

    Provides validation for service creation and updates, including
    name uniqueness checks and price range validation.
    """

    @staticmethod
    def _find_service_by_name(name: str) -> Optional['Service']:
        """
        Search for a service by name.

        Args:
            name (str): The service name to search for.

        Returns:
            Optional[Service]: The service object if found, otherwise None.
        """

        return get_service_by_name(name)

    @staticmethod
    def _validate_price_range(price: int) -> None:
        """
        Validate that price is within the allowed range.

        Args:
            price (int): The price in cents.

        Raises:
            HTTPException: If price is outside valid range (422).
        """
        if not MIN_SERVICE_PRICE <= price <= MAX_SERVICE_PRICE:
            BaseValidation.abort_with_error(
                422,  f'Price must be between {MIN_SERVICE_PRICE} '
                f'and {MAX_SERVICE_PRICE} cents.', 'price')

    @staticmethod
    def _validate_status(status: str) -> None:
        """
        Validate that status is one of the allowed values.

        Args:
            status (str): The status value.

        Raises:
            HTTPException: If status is not valid (422).
        """
        if status not in ALLOWED_STATUS_VALUES:
            BaseValidation.abort_with_error(
                422, f'Status must be one of: {", ".join(ALLOWED_STATUS_VALUES)}.', 'status')

    @staticmethod
    def _validate_name_unique(name: str, exclude_id: Optional[int] = None) -> None:
        """
        Validate that a service name is not already registered.

        Args:
            name (str): The service name to check.
            exclude_id (Optional[int]): Service ID to exclude from the check (for updates).

        Raises:
            HTTPException: If name is already registered (409).
        """
        existing = ServiceValidation._find_service_by_name(name)
        if existing is None:
            return

        if exclude_id is not None and getattr(existing, 'id', None) == exclude_id:
            return

        BaseValidation.abort_with_error(
            409, 'Service already registered.', 'name')

    @staticmethod
    def validate_service(name: str, price: int, status: str = 'available') -> None:
        """
        Validate a new service's data.

        Args:
            name (str): The service's name.
            price (int): The service's price in cents.
            status (str): The service's status.

        Raises:
            HTTPException: If name is taken (409), price is invalid (422), or status is invalid (422).
        """
        ServiceValidation._validate_name_unique(name)
        ServiceValidation._validate_price_range(price)
        ServiceValidation._validate_status(status)

    @staticmethod
    def validate_service_update(
        fields: dict,
        current_service_id: Optional[int] = None
    ) -> dict:
        """
        Validate update payload and check uniqueness constraints.

        Args:
            fields (dict): Raw update payload.
            current_service_id (Optional[int]): ID of the service being updated. If provided,
                allows the same name if it belongs to this service.

        Returns:
            dict: Cleaned fields ready to apply.

        Raises:
            HTTPException: For uniqueness conflicts (409) or invalid price (422).
        """
        cleaned = BaseValidation.validate_update_payload(
            fields, allowed_update_fields=ALLOWED_UPDATE_FIELDS
        )

        if 'name' in cleaned:
            ServiceValidation._validate_name_unique(
                cleaned['name'], exclude_id=current_service_id
            )

        if 'price' in cleaned:
            ServiceValidation._validate_price_range(cleaned['price'])

        if 'status' in cleaned:
            ServiceValidation._validate_status(cleaned['status'])

        return cleaned

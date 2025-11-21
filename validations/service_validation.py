"""
Validation module for Service entities.
"""

from typing import Optional
from flask_smorest import abort
from repositories.service_repository import get_service_by_name
from validations.base import BaseValidation

MAX_SERVICE_PRICE = 10000
MIN_SERVICE_PRICE = 2500

ALLOWED_UPDATE_FIELDS = {'name': str, 'price': int}


class ServiceValidation:
    """
    Validation class for Service entities.

    Provides validation for service creation and updates, including
    name uniqueness checks and price range validation.
    """

    @staticmethod
    def _find_service_by_name(name: str) -> Optional[object]:
        """
        Search for a service by name.

        Args:
            name: The service name to search for.

        Returns:
            The service object if found, otherwise None.
        """
        return get_service_by_name(name)

    @staticmethod
    def _validate_price_range(price: int) -> None:
        """
        Validate that price is within the allowed range.

        Args:
            price: The price in cents.

        Raises:
            HTTPException: If price is outside valid range (422).
        """
        if not MIN_SERVICE_PRICE <= price <= MAX_SERVICE_PRICE:
            abort(422, errors={
                'json': {
                    'price': [
                        f'Price must be between {MIN_SERVICE_PRICE} and {MAX_SERVICE_PRICE} cents.'
                    ]
                }
            })

    @staticmethod
    def _validate_name_unique(name: str, exclude_id: Optional[int] = None) -> None:
        """
        Validate that a service name is not already registered.

        Args:
            name: The service name to check.
            exclude_id: Service ID to exclude from the check (for updates).

        Raises:
            HTTPException: If name is already registered (409).
        """
        existing = ServiceValidation._find_service_by_name(name)
        if existing is None:
            return

        if exclude_id is not None and getattr(existing, 'id', None) == exclude_id:
            return

        abort(409, errors={'json': {'name': ['Service already registered.']}})

    @staticmethod
    def validate_service(name: str, price: int) -> None:
        """
        Validate a new service's data.

        Args:
            name: The service's name.
            price: The service's price in cents.

        Raises:
            HTTPException: If name is taken (409) or price is invalid (422).
        """
        ServiceValidation._validate_name_unique(name)
        ServiceValidation._validate_price_range(price)

    @staticmethod
    def validate_service_update(
        fields: dict,
        current_service_id: Optional[int] = None
    ) -> dict:
        """
        Validate update payload and check uniqueness constraints.

        Args:
            fields: Raw update payload.
            current_service_id: ID of the service being updated. If provided,
                allows the same name if it belongs to this service.

        Returns:
            Cleaned fields ready to apply.

        Raises:
            BadRequest: For invalid payloads.
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

        return cleaned

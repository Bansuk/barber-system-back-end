"""
Business module for Service entities.
"""

from datetime import datetime
from business.base import get_or_404
from database.models.service import Service
from repositories.service_repository import add_service, delete_service, get_service, update_service
from validations.base import BaseValidation
from validations.service_validation import ServiceValidation


def create_service(name: str, price: int, status: str = 'available') -> Service:
    """
    Creates a new Service.

    Args:
        name (str): The service's name.
        price (int): The service's price in cents.
        status (str): The service's status ('available' or 'unavailable').

    Returns:
        Service: Created service.
    """

    ServiceValidation.validate_service(name, price, status)

    return add_service(name, price, status)


def get_service_by_id(service_id: int) -> Service:
    """
    Retrieves a service by its ID.

    Args:
        service_id (int): The service's unique identifier.

    Returns:
        service: The service found.

    Raises:
        HTTPException: If service not found (404) or invalid ID (400).
    """

    return get_or_404(get_service, service_id, 'service')


def delete_service_by_id(service_id: int) -> bool:
    """
    Deletes an existing service by its ID.

    Args:
        service_id (int): The service's unique identifier.

    Returns:
        bool: True if the service was successfully deleted.

    Raises:
        HTTPException: If service not found (404) or invalid ID (400).
    """

    service = get_or_404(get_service, service_id, 'service')

    return delete_service(service)


def update_service_by_id(service_id: int, **fields) -> Service:
    """
    Updates an existing service by its ID using keyword fields.

    Args:
        service_id (int): The service's unique identifier.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        service: Updated service.

    Raises:
        HTTPException: If service not found (404) or validation fails.
    """

    service = get_or_404(get_service, service_id, 'service')

    validated = ServiceValidation.validate_service_update(
        fields, current_service_id=service_id)

    return update_service(service, **validated)

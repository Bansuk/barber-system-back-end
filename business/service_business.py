"""
Business module for Service entities.
"""

from flask_smorest import abort
from database.models.service import Service
from repositories.service_repository import add_service, delete_service, get_service, update_service
from validations.base import BaseValidation
from validations.service_validation import ServiceValidation


def create_service(name: str, price: int) -> Service:
    """
    Creates a new Service.

    Args:
        name (str): The service's name.
        price (int): The service's price in cents.

    Returns:
        Service: Created service.
    """

    ServiceValidation.validate_service(name, price)

    add_service(name, price)


def delete_service_by_id(service_id: int) -> bool:
    """
    Deletes an existing service by its ID.

    Args:
        service_id (int): The service's unique identifier.

    Returns:
        bool: True if the service was successfully deleted.

    Raises:
        werkzeug.exceptions.NotFound: If the service does not exist.
        Exception: If an unexpected error occurs during deletion.
    """

    try:
        BaseValidation.validate_positive_int(service_id, 'service')

        service = get_service(service_id)
        if service is None:
            abort(404, errors={'json': ['Service not found.']})

        return delete_service(service)
    except Exception as error:
        raise error


def update_service_by_id(service_id: int, **fields) -> Service:
    """
    Updates an existing service by its ID using keyword fields.

    Args:
        service_id (int): The service's unique identifier.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        service: Updated service.

    Raises:
        werkzeug.exceptions.NotFound: If the service does not exist.
        HTTPException: If validation fails.
        Exception: If an unexpected error occurs during update.
    """

    try:
        BaseValidation.validate_positive_int(service_id, 'service')

        service = get_service(service_id)
        if service is None:
            abort(404, errors={'json': ['Service not found.']})

        updates = ServiceValidation.validate_service_update(
            fields, current_service_id=service_id)

        return update_service(service, **updates)
    except Exception as error:
        raise error

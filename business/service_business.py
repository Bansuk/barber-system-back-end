"""
Business module for Service entities.
"""

from flask_smorest import abort
from database.models.service import Service
from database.db_setup import db
from repositories.service_repository import delete_service, get_service
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

    service = Service(name=name, price=price, employees=[], appointments=[])

    try:
        db.session.add(service)
        db.session.commit()

        return service
    except Exception as error:
        db.session.rollback()
        raise error


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

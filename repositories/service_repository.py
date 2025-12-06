"""
Repository module for Service queries.
"""

from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from database.models.service import Service
from database.db_setup import db


def get_all_services() -> List[Service]:
    """
    Retrieves all registered services.

    Returns:
        List[Service]: A List of registered services.
    """

    return db.session.query(Service).all()


def get_services_by_services_ids(services_ids: List[int]) -> List[Service]:
    """
    Retrieves all registered services by ID's.

    Args:
        services_ids (List[int]): The services ID's to search.

    Returns:
        List[Service]: A List of registered services.
    """

    return db.session.query(Service).filter(Service.id.in_(services_ids)).all()


def get_services_count() -> int:
    """
    Retrieves the number of registered services.

    Returns:
        int: The total number of services.
    """

    return db.session.query(Service).count()


def get_service(service_id: int) -> Optional[Service]:
    """
    Retrieves a service by its ID.

    Args:
        service_id (int): The service ID.

    Returns:
        Optional[Service]: The service found or None.
    """

    return db.session.query(Service).filter_by(id=service_id).first()


def get_service_by_name(name: str) -> Optional[Service]:
    """
    Retrieves a service by its name.

    Args:
        name (str): The service name.

    Returns:
        Optional[Service]: The service found or None.
    """

    return db.session.query(Service).filter_by(name=name).first()


def delete_service(service: Service) -> bool:
    """
    Deletes the given service from the database.

    Args:
        service (Service): The service to delete.

    Returns:
        bool: True if the service was deleted successfully.

    Raises:
        SQLAlchemyError: If the deletion fails.
    """

    try:
        db.session.delete(service)
        db.session.commit()

        return True
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def add_service(name: str, price: int) -> Service:
    """
    Adds a new service to the database.

    Args:
        name (str): The service's name.
        price (int): The service's price in cents.

    Returns:
        Service: Created service.

    Raises:
        SQLAlchemyError: If the addition fails.
    """

    try:
        service = Service(name=name, price=price,
                          employees=[], appointments=[])
        db.session.add(service)
        db.session.commit()

        return service
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def update_service(service: Service, **fields) -> Service:
    """
    Updates an existing service in the database.

    Args:
        service (Service): The service to update.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        Service: Updated service.

    Raises:
        SQLAlchemyError: If the update fails.
    """

    try:
        for key, value in fields.items():
            if hasattr(service, key) and value is not None:
                setattr(service, key, value)

        db.session.add(service)
        db.session.commit()

        return service
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error

"""
Repository module for Appointment queries.
"""

from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from database.db_setup import db
from database.models.appointment import Appointment

if TYPE_CHECKING:
    from ..database.models.appointment import Appointment
    from ..database.models.service import Service


def get_all_appointments() -> List[Appointment]:
    """
    Retrieves all registered appointments.

    Returns:
        List[Appointment]: A list of registered appointments.
    """

    return db.session.query(Appointment).all()


def get_appointments_count(period: Optional[str] = None) -> int:
    """
    Retrieves the number of registered appointments.

    Args:
        period (Optional[str]): Filter by time period ('all', 'past', 'upcoming').
                                If None or 'all', returns all appointments.

    Returns:
        int: The total number of appointments.
    """

    query = db.session.query(Appointment)
    
    if period == 'past':
        query = query.filter(Appointment.date < datetime.now())
    elif period == 'upcoming':
        query = query.filter(Appointment.date >= datetime.now())
    
    return query.count()


def get_appointment(appointment_id: int) -> Optional[Appointment]:
    """
    Retrieves an appointment by its ID.

    Args:
        appointment_id (int): The appointment ID.

    Returns:
         Optional[Appointment] | None: The appointment found or None.
    """

    return db.session.query(Appointment).filter_by(id=appointment_id).first()


def get_customer_appointment(date: datetime, customer_id: int, exclude_appointment_id: Optional[int] = None) -> Optional[Appointment]:
    """
    Retrieves a customer appointment by date.

    Args:
        date (datetime): The appointment date.
        customer_id (int): The customer's ID.
        exclude_appointment_id (Optional[int]): Appointment ID to exclude from the search (for updates).

    Returns:
         Optional[Appointment]: The appointment found or None.
    """

    query = db.session.query(Appointment).filter(
        Appointment.customer_id == customer_id,
        Appointment.date == date
    )
    
    if exclude_appointment_id is not None:
        query = query.filter(Appointment.id != exclude_appointment_id)
    
    return query.first()


def get_employee_appointment(date: datetime, employee_id: int, exclude_appointment_id: Optional[int] = None) -> Optional[Appointment]:
    """
    Retrieves an employee appointment by date.

    Args:
        date (datetime): The appointment date.
        employee_id (int): The employee's ID.
        exclude_appointment_id (Optional[int]): Appointment ID to exclude from the search (for updates).

    Returns:
         Optional[Appointment]: The appointment found or None.
    """

    query = db.session.query(Appointment).filter(
        Appointment.employee_id == employee_id,
        Appointment.date == date
    )
    
    if exclude_appointment_id is not None:
        query = query.filter(Appointment.id != exclude_appointment_id)
    
    return query.first()


def delete_appointment(appointment: Appointment) -> bool:
    """
    Deletes the given appointment from the database.

    Args:
        appointment (Appointment): The appointment to delete.

    Returns:
        bool: True if the appointment was deleted successfully.

    Raises:
        SQLAlchemyError: If the deletion fails.
    """

    try:
        db.session.delete(appointment)
        db.session.commit()

        return True
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def add_appointment(date: str, customer_id: int,
                    employee_id: int, services: List['Service']) -> Appointment:
    """
    Adds a new appointment to the database.

    Args:
        date (str): The appointment's date.
        customer_id (int): The customer's ID.
        employee_id (int): The employee's ID.
        services (List[Service]): List of services for the appointment.

    Returns:
        Appointment: Created appointment.

    Raises:
        SQLAlchemyError: If the addition fails.
    """

    try:
        appointment = Appointment(date, services, employee_id, customer_id)
        db.session.add(appointment)
        db.session.commit()

        return appointment
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def update_appointment(appointment: Appointment, **fields) -> Appointment:
    """
    Updates an existing appointment in the database.

    Args:
        appointment (Appointment): The appointment to update.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        Appointment: Updated appointment.

    Raises:
        SQLAlchemyError: If the update fails.
    """

    try:
        for key, value in fields.items():
            if hasattr(appointment, key) and value is not None:
                setattr(appointment, key, value)

        db.session.add(appointment)
        db.session.commit()

        return appointment
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error

"""
Business module for Appointment entities.
"""

from datetime import datetime
from typing import List
from business.base import get_or_404
from database.models.appointment import Appointment
from repositories.appointment_repository import add_appointment, delete_appointment, \
    get_appointment, update_appointment
from repositories.service_repository import get_service
from validations.appointment_validation import AppointmentValidation


def create_appointment(date: str, customer_id: int,
                       employee_id: int, services_ids: List[int]) -> Appointment:
    """
    Creates a new appointment.

    Args:
        date (str): The appointment's date.
        customer_id (int): The customer's ID who booked the appointment.
        employee_id (int): The employee's ID who will execute the appointment.
        services_ids (List[int]): The list of services IDs that will be executed.

    Returns:
        Appointment: Created appointment.
    """

    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    AppointmentValidation.validate_appointment(date,
                                               customer_id, employee_id, services_ids)

    services = [get_service(service_id) for service_id in services_ids]

    return add_appointment(date, customer_id, employee_id, services)


def delete_appointment_by_id(appointment_id: int) -> bool:
    """
    Deletes an existing appointment by its ID.

    Args:
        appointment_id (int): The appointment's unique identifier.

    Returns:
        bool: True if the appointment was successfully deleted.

    Raises:
        HTTPException: If appointment not found (404) or invalid ID (400).
    """

    appointment = get_or_404(get_appointment, appointment_id, 'appointment')

    return delete_appointment(appointment)


def update_appointment_by_id(appointment_id: int, **fields) -> Appointment:
    """
    Update an existing appointment by its ID.

    Args:
        appointment_id: The appointment's unique identifier.
        **fields: Fields to update (date, customer_id, employee_id, service_ids).

    Returns:
        The updated appointment.

    Raises:
        HTTPException: If appointment not found (404) or validation fails.
    """
    appointment = get_or_404(get_appointment, appointment_id, 'appointment')

    validated = AppointmentValidation.validate_appointment_update(
        fields,
        current_customer_id=appointment.customer_id,
        current_employee_id=appointment.employee_id,
        current_date=appointment.date
    )

    return update_appointment(appointment, **validated)

"""
Business module for Appointment entities.
"""

from typing import List
from datetime import datetime
from flask_smorest import abort
from database.models.appointment import Appointment
from repositories.appointment_repository import get_appointment
from repositories.appointment_repository import add_appointment, delete_appointment, get_appointment, update_appointment
from validations.appointment_validation import AppointmentValidation
from validations.base import BaseValidation


def create_appointment(date: str, customer_id: int,
                       employee_id: int, appointments_ids: List[int]) -> Appointment:
    """
    Creates a new appointment.

    Args:
        date (str): The appointment's date.
        customer_id (int): The customer's ID who booked the appointment.
        employee_id (int): The employee's ID who will execute the appointment.
        appointments_ids (List[int]): The list of appointment IDs that will be executed.

    Returns:
        Appointment: Created appointment.
    """

    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    AppointmentValidation.validate_appointment(date,
                                               customer_id, employee_id, appointments_ids)

    appointments = [get_appointment(appointment_id)
                    for appointment_id in appointments_ids]

    return add_appointment(date, customer_id, employee_id, appointments)


def delete_appointment_by_id(appointment_id: int) -> bool:
    """
    Deletes an existing appointment by its ID.

    Args:
        appointment_id (int): The appointment's unique identifier.

    Returns:
        bool: True if the appointment was successfully deleted.

    Raises:
        werkzeug.exceptions.NotFound: If the appointment does not exist.
        Exception: If an unexpected error occurs during deletion.
    """

    try:
        BaseValidation.validate_positive_int(appointment_id, 'appointment')

        appointment = get_appointment(appointment_id)
        if appointment is None:
            abort(404, errors={'json': ['appointment not found.']})

        return delete_appointment(appointment)
    except Exception as error:
        raise error


def update_appointment_by_id(appointment_id: int, **fields) -> Appointment:
    """
    Update an existing appointment by its ID.

    Args:
        appointment_id: The appointment's unique identifier.
        **fields: Fields to update (date, employee_id, service_ids).

    Returns:
        The updated appointment.

    Raises:
        HTTPException: If appointment not found (404) or validation fails.
    """
    BaseValidation.validate_positive_int(appointment_id, 'appointment')

    appointment = get_appointment(appointment_id)
    if appointment is None:
        abort(404, errors={
              'json': {'appointment': ['Appointment not found.']}})

    validated = AppointmentValidation.validate_appointment_update(
        fields,
        current_customer_id=appointment.customer_id,
        current_employee_id=appointment.employee_id,
        current_date=appointment.date
    )

    return update_appointment(appointment, **validated)

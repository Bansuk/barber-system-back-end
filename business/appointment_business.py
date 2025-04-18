"""
Business module for Appointment entities.
"""

from typing import List
from datetime import datetime
from database.db_setup import db
from database.models.appointment import Appointment
from repositories.service_repository import get_service
from validations.appointment_validation import AppointmentValidation


def create_appointment(date: str, customer_id: int,
                       employee_id: int, services_ids: List[int]) -> Appointment:
    """
    Creates a new appointment.

    Args:
        date (str): The appointment's date.
        customer_id (int): The customer's ID who booked the service.
        employee_id (int): The employee's ID who will execute the service.
        services_ids (List[int]): The list of service IDs that will be executed.

    Returns:
        Appointment: Created appointment.
    """

    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    AppointmentValidation.validate_appointment(date,
                                               customer_id, employee_id, services_ids)

    services = [get_service(service_id) for service_id in services_ids]

    appointment = Appointment(date, services,
                              employee_id, customer_id)

    try:
        db.session.add(appointment)
        db.session.commit()

        return appointment
    except Exception as error:
        db.session.rollback()
        raise error

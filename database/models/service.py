"""
This module defines the Service model for the database.
"""

from typing import TYPE_CHECKING
from datetime import datetime, timezone
from enum import Enum
from database.db_setup import db
from .service_appointment import service_appointment
from .service_employee import service_employee

if TYPE_CHECKING:
    from database.models.appointment import Appointment
    from database.models.employee import Employee


class ServiceStatus(Enum):
    """
    Enum for service status values.
    """

    AVAILABLE = 'available'
    UNAVAILABLE = 'unavailable'


class Service(db.Model):
    """
    Represents a service entity in the database.

    Attributes:
        id (int): Primary key identifier.
        name (str): Name of the service.
        price (int): Price of the service in cents.
        status (str): Status of the service ('available' or 'unavailable').
        employees (list): List of employees that can perform the service.
        appointments (list): List of appointments with assigned service.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
    """
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default=ServiceStatus.AVAILABLE.value)
    employees = db.relationship(
        'Employee', secondary=service_employee, back_populates='services')
    appointments = db.relationship(
        'Appointment', secondary=service_appointment, back_populates='services')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, name: str, price: int,
                 employees: list['Employee'], appointments: list['Appointment'],
                 status: str = ServiceStatus.AVAILABLE.value) -> None:
        self.name = name
        self.price = price
        self.status = status
        self.employees = employees
        self.appointments = appointments

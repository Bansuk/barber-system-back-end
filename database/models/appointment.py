"""
This module defines the Appointment model for the database.
"""

from typing import List, TYPE_CHECKING
from datetime import datetime, timezone
from database.db_setup import db
from .service_appointment import service_appointment


if TYPE_CHECKING:
    from .service import Service


class Appointment(db.Model):
    """
    Represents an appointment entity in the database.

    Attributes:
        id (int): Primary key identifier.
        date (datetime): Date and time of the appointment.
        services (List[Service]): List of services associated with the appointment.
        employee_id (int): Foreign key referencing the assigned employee.
        customer_id (int): Foreign key referencing the assigned customer.
        created_at (datetime): Timestamp when the record was created.
        updated_at (datetime): Timestamp when the record was last updated.
    """

    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    services = db.relationship(
        'Service', secondary=service_appointment, back_populates='appointments')
    employee_id = db.Column(db.Integer, db.ForeignKey(
        'employee.id'), nullable=False)
    employee = db.relationship('Employee', back_populates='appointments')
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    customer = db.relationship('Customer', back_populates='appointments')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, date: datetime, services: List['Service'],
                 employee_id: int, customer_id: int) -> None:
        self.date = date
        self.services = services
        self.employee_id = employee_id
        self.customer_id = customer_id

"""Validation module for Appointment entities."""

from datetime import datetime, timedelta, time
from typing import Optional
from flask_smorest import abort
from werkzeug.exceptions import BadRequest
from repositories.employee_repository import get_employee
from repositories.customer_repository import get_customer
from repositories.service_repository import get_service
from repositories.appointment_repository import (
    get_customer_appointment,
    get_employee_appointment
)

MAX_ADVANCE_DAYS = 7
OPENING_TIME = time(9, 0)
CLOSING_TIME = time(18, 0)

ALLOWED_UPDATE_FIELDS = {'date': datetime,
                         'employee_id': int, 'service_ids': list}


class AppointmentValidation:
    """
    Validation class for Appointment entities.

    Provides validation for appointment creation, including date/time
    validation, entity existence checks, and availability verification.
    """

    @staticmethod
    def _validate_date_range(date: datetime) -> None:
        """
        Validate that the appointment date is within the allowed range.

        Args:
            date: The appointment's date.

        Raises:
            HTTPException: If date is outside allowed range (400).
        """
        now = datetime.now()
        max_date = now + timedelta(days=MAX_ADVANCE_DAYS)

        if not now <= date <= max_date:
            abort(400, errors={
                'json': {
                    'date': [f'Date must be between now and {MAX_ADVANCE_DAYS} days in advance.']
                }
            })

    @staticmethod
    def _validate_business_hours(date: datetime) -> None:
        """
        Validate that the appointment time is within business hours.

        Args:
            date: The appointment's date.

        Raises:
            HTTPException: If time is outside business hours (400).
        """
        if not OPENING_TIME <= date.time() < CLOSING_TIME:
            opening = OPENING_TIME.strftime('%H:%M')
            closing = CLOSING_TIME.strftime('%H:%M')
            abort(400, errors={
                'json': {
                    'date': [f'Appointments must be between {opening} and {closing}.']
                }
            })

    @staticmethod
    def _validate_date_available(
        date: datetime,
        employee_id: int,
        customer_id: int
    ) -> None:
        """
        Validate that the time slot is available for both customer and employee.

        Args:
            date: The appointment's date.
            employee_id: The employee's ID.
            customer_id: The customer's ID.

        Raises:
            HTTPException: If the time slot is already booked (409).
        """
        if get_customer_appointment(date, customer_id):
            abort(409, errors={
                'json': {'date': ['Customer already has an appointment at this time.']}
            })

        if get_employee_appointment(date, employee_id):
            abort(409, errors={
                'json': {'date': ['Employee already has an appointment at this time.']}
            })

    @staticmethod
    def _get_validated_services(service_ids: list[int]) -> list:
        """
        Validate and retrieve Service objects for the given IDs.

        Args:
            service_ids: List of service IDs to validate.

        Returns:
            List of Service objects.

        Raises:
            HTTPException: If any service is not found (404).
        """
        if not service_ids:
            abort(400, errors={'json': {'service_ids': [
                  'At least one service is required.']}})

        services = []
        for service_id in service_ids:
            service = get_service(service_id)
            if service is None:
                abort(404, errors={
                    'json': {'service_ids': [f'Service with ID {service_id} not found.']}
                })
            services.append(service)

        return services

    @staticmethod
    def _get_validated_employee(employee_id: int) -> object:
        """
        Validate and retrieve the Employee object.

        Args:
            employee_id: The employee's ID.

        Returns:
            The Employee object.

        Raises:
            HTTPException: If employee is not found (404).
        """
        employee = get_employee(employee_id)
        if employee is None:
            abort(404, errors={
                'json': {'employee_id': [f'Employee with ID {employee_id} not found.']}
            })
        return employee

    @staticmethod
    def _get_validated_customer(customer_id: int) -> object:
        """
        Validate and retrieve the Customer object.

        Args:
            customer_id: The customer's ID.

        Returns:
            The Customer object.

        Raises:
            HTTPException: If customer is not found (404).
        """
        customer = get_customer(customer_id)
        if customer is None:
            abort(404, errors={
                'json': {'customer_id': [f'Customer with ID {customer_id} not found.']}
            })
        return customer

    @staticmethod
    def validate_appointment(
        date: datetime,
        customer_id: int,
        employee_id: int,
        service_ids: list[int]
    ) -> dict:
        """
        Validate a new appointment's data.

        Args:
            date: The appointment's date and time.
            customer_id: The customer's ID.
            employee_id: The employee's ID.
            service_ids: List of service IDs for the appointment.

        Returns:
            Dictionary containing validated entities:
                - customer: The Customer object
                - employee: The Employee object
                - services: List of Service objects

        Raises:
            HTTPException: If any validation fails (400, 404, or 409).
        """
        # Validate entities first (fail fast if IDs are invalid)
        customer = AppointmentValidation._get_validated_customer(customer_id)
        employee = AppointmentValidation._get_validated_employee(employee_id)
        services = AppointmentValidation._get_validated_services(service_ids)

        # Then validate date/time constraints
        AppointmentValidation._validate_date_range(date)
        AppointmentValidation._validate_business_hours(date)
        AppointmentValidation._validate_date_available(
            date, employee_id, customer_id)

        return {
            'customer': customer,
            'employee': employee,
            'services': services
        }

    @staticmethod
    def _validate_update_payload(payload: dict) -> dict:
        """
        Validate and clean the update payload.

        Args:
            payload: Raw update data.

        Returns:
            Cleaned dictionary with only valid fields.

        Raises:
            BadRequest: If payload contains invalid types or no valid fields.
        """
        cleaned = {}

        for field, expected_type in ALLOWED_UPDATE_FIELDS.items():
            value = payload.get(field)
            if value is None:
                continue

            # Special handling for datetime (may come as string)
            if expected_type == datetime:
                if isinstance(value, datetime):
                    cleaned[field] = value
                elif isinstance(value, str):
                    try:
                        cleaned[field] = datetime.fromisoformat(value)
                    except ValueError:
                        raise BadRequest(
                            description=f"Field '{field}' must be a valid ISO datetime string."
                        )
                else:
                    raise BadRequest(
                        description=f"Field '{field}' must be a datetime or ISO string."
                    )
            elif not isinstance(value, expected_type):
                raise BadRequest(
                    description=f"Field '{field}' must be of type {expected_type.__name__}."
                )
            else:
                cleaned[field] = value

        if not cleaned:
            raise BadRequest(description='No valid fields to update.')

        return cleaned

    @staticmethod
    def validate_appointment_update(
        fields: dict,
        current_customer_id: int,
        current_employee_id: Optional[int] = None,
        current_date: Optional[datetime] = None
    ) -> dict:
        """
        Validate update payload and check constraints.

        Args:
            fields: Raw update payload.
            current_customer_id: ID of the customer (cannot be changed).
            current_employee_id: Current employee ID (for availability check).
            current_date: Current appointment date (for availability check).

        Returns:
            Cleaned fields with validated entities ready to apply:
                - date: The validated datetime (if provided)
                - employee: The Employee object (if employee_id provided)
                - services: List of Service objects (if service_ids provided)

        Raises:
            BadRequest: For invalid payloads.
            HTTPException: For not found (404) or conflicts (409).
        """
        cleaned = AppointmentValidation._validate_update_payload(fields)
        result = {}

        # Validate and convert employee_id to employee object
        if 'employee_id' in cleaned:
            result['employee'] = AppointmentValidation._get_validated_employee(
                cleaned['employee_id']
            )
            employee_id = cleaned['employee_id']
        else:
            employee_id = current_employee_id

        # Validate and convert service_ids to service objects
        if 'service_ids' in cleaned:
            result['services'] = AppointmentValidation._get_validated_services(
                cleaned['service_ids']
            )

        # Validate date constraints and availability
        if 'date' in cleaned:
            date = cleaned['date']
            AppointmentValidation._validate_date_range(date)
            AppointmentValidation._validate_business_hours(date)
            AppointmentValidation._validate_date_available(
                date, employee_id, current_customer_id
            )
            result['date'] = date
        elif employee_id != current_employee_id and current_date:
            # Employee changed but date didn't - check new employee's availability
            AppointmentValidation._validate_date_available(
                current_date, employee_id, current_customer_id
            )

        return result

"""
Validation module for Appointment entities.
"""

from datetime import datetime, timedelta, time
from typing import Optional
from repositories.employee_repository import get_employee
from repositories.customer_repository import get_customer
from repositories.service_repository import get_service
from repositories.appointment_repository import (
    get_customer_appointment,
    get_employee_appointment
)
from validations.base import BaseValidation

MAX_ADVANCE_DAYS = 7
OPENING_TIME = time(9, 0)
CLOSING_TIME = time(18, 0)

ALLOWED_UPDATE_FIELDS = {'date': datetime,
                         'employee_id': int, 'services_ids': list}


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
            date (datetime): The appointment's date.

        Raises:
            HTTPException: If date is outside allowed range (400).
        """
        now = datetime.now()
        max_date = now + timedelta(days=MAX_ADVANCE_DAYS)

        if not now <= date <= max_date:
            BaseValidation.abort_with_error(
                400, f'Date must be between now and {MAX_ADVANCE_DAYS} days in advance.', 'date')

    @staticmethod
    def _validate_business_hours(date: datetime) -> None:
        """
        Validate that the appointment time is within business hours.

        Args:
            date (datetime): The appointment's date.

        Raises:
            HTTPException: If time is outside business hours (400).
        """
        if not OPENING_TIME <= date.time() < CLOSING_TIME:
            opening = OPENING_TIME.strftime('%H:%M')
            closing = CLOSING_TIME.strftime('%H:%M')
            BaseValidation.abort_with_error(
                400, f'Appointments must be between {opening} and {closing}.', 'date')

    @staticmethod
    def _validate_date_available(
        date: datetime,
        employee_id: int,
        customer_id: int,
        exclude_appointment_id: Optional[int] = None
    ) -> None:
        """
        Validate that the time slot is available for both customer and employee.

        Args:
            date (datetime): The appointment's date.
            employee_id (int): The employee's ID.
            customer_id (int): The customer's ID.
            exclude_appointment_id (Optional[int]): Appointment ID to exclude from check (for updates).

        Raises:
            HTTPException: If the time slot is already booked (409).
        """
        if get_customer_appointment(date, customer_id, exclude_appointment_id):
            BaseValidation.abort_with_error(
                409, 'Customer already has an appointment at this time.', 'date')

        if get_employee_appointment(date, employee_id, exclude_appointment_id):
            BaseValidation.abort_with_error(
                409, 'Employee already has an appointment at this time.', 'date')

    @staticmethod
    def _get_validated_services(service_ids: list[int]) -> list:
        """
        Validate and retrieve Service objects for the given IDs.

        Args:
            service_ids (list[int]): List of service IDs to validate.

        Returns:
            list: List of Service objects.

        Raises:
            HTTPException: If services was not provided (400) or if any service is not found (404).
        """
        if not service_ids:
            BaseValidation.abort_with_error(
                400, 'At least one service is required.', 'service_ids')

        services = []
        for service_id in service_ids:
            service = get_service(service_id)
            if service is None:
                BaseValidation.abort_with_error(
                    404, f'Service with ID {service_id} not found.', 'service_ids')
            services.append(service)

        return services

    @staticmethod
    def _get_validated_employee(employee_id: int) -> object:
        """
        Validate and retrieve the Employee object.

        Args:
            employee_id (int): The employee's ID.

        Returns:
            object: The Employee object.

        Raises:
            HTTPException: If employee is not found (404).
        """
        employee = get_employee(employee_id)
        if employee is None:
            BaseValidation.abort_with_error(
                404, f'Employee with ID {employee_id} not found.', 'employee_id')

        return employee

    @staticmethod
    def _get_validated_customer(customer_id: int) -> object:
        """
        Validate and retrieve the Customer object.

        Args:
            customer_id (int): The customer's ID.

        Returns:
            object: The Customer object.

        Raises:
            HTTPException: If customer is not found (404).
        """
        customer = get_customer(customer_id)
        if customer is None:
            BaseValidation.abort_with_error(
                404, f'Customer with ID {customer_id} not found.', 'customer_id')

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
            date (datetime): The appointment's date and time.
            customer_id (int): The customer's ID.
            employee_id (int): The employee's ID.
            service_ids (list[int]): List of service IDs for the appointment.

        Returns:
            dict: Dictionary containing validated entities:
                - customer: The Customer object
                - employee: The Employee object
                - services: List of Service objects

        Raises:
            HTTPException: If any validation fails (400, 404, or 409).
        """
        customer = AppointmentValidation._get_validated_customer(customer_id)
        employee = AppointmentValidation._get_validated_employee(employee_id)
        services = AppointmentValidation._get_validated_services(service_ids)

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
            payload (dict): Raw update data.

        Returns:
            dict: Cleaned dictionary with only valid fields.

        Raises:
            HTTPException: If payload contains invalid types or no valid fields (400).
        """
        cleaned = {}

        for field, expected_type in ALLOWED_UPDATE_FIELDS.items():
            value = payload.get(field)
            if value is None:
                continue

            if expected_type == datetime:
                if isinstance(value, datetime):
                    cleaned[field] = value
                elif isinstance(value, str):
                    try:
                        cleaned[field] = datetime.fromisoformat(value)
                    except ValueError:
                        BaseValidation.abort_with_error(
                            400, f"Field '{field}' must be a valid ISO datetime string.", field)
                else:
                    BaseValidation.abort_with_error(
                        400, f"Field '{field}' must be a datetime or ISO string.", field)
            elif not isinstance(value, expected_type):
                BaseValidation.abort_with_error(
                    400, f"Field '{field}' must be of type {expected_type.__name__}.", field)
            else:
                cleaned[field] = value

        if not cleaned:
            BaseValidation.abort_with_error(
                400, 'No valid fields to update.')

        return cleaned

    @staticmethod
    def validate_appointment_update(
        fields: dict,
        current_customer_id: int,
        current_employee_id: Optional[int] = None,
        current_date: Optional[datetime] = None,
        appointment_id: Optional[int] = None
    ) -> dict:
        """
        Validate update payload and check constraints.

        Args:
            fields (dict): Raw update payload.
            current_customer_id (int): ID of the customer (cannot be changed).
            current_employee_id (Optional[int]): Current employee ID (for availability check).
            current_date (Optional[datetime]): Current appointment date (for availability check).
            appointment_id (Optional[int]): ID of the appointment being updated (to exclude from checks).

        Returns:
            dict: Cleaned fields with validated entities ready to apply:
                    - date: The validated datetime (if provided)
                    - employee: The Employee object (if employee_id provided)
                    - services: List of Service objects (if service_ids provided)

        Raises:
            HTTPException: For not found (404) or conflicts (409).
        """
        cleaned = AppointmentValidation._validate_update_payload(fields)
        result = {}

        if 'employee_id' in cleaned:
            result['employee'] = AppointmentValidation._get_validated_employee(
                cleaned['employee_id']
            )
            employee_id = cleaned['employee_id']
        else:
            employee_id = current_employee_id

        if 'services_ids' in cleaned:
            result['services'] = AppointmentValidation._get_validated_services(
                cleaned['services_ids']
            )

        if 'date' in cleaned:
            date = cleaned['date']
            AppointmentValidation._validate_date_range(date)
            AppointmentValidation._validate_business_hours(date)
            AppointmentValidation._validate_date_available(
                date, employee_id, current_customer_id, appointment_id
            )
            result['date'] = date
        elif employee_id != current_employee_id and current_date:
            AppointmentValidation._validate_date_available(
                current_date, employee_id, current_customer_id, appointment_id
            )

        return result

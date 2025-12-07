"""
Validation module for Employee entities.
"""

from typing import Optional, TYPE_CHECKING
from repositories.service_repository import get_services_count, get_service
from repositories.employee_repository import search_employee_email, search_employee_by_phone_number
from validations.base import BaseValidation

if TYPE_CHECKING:
    from ..database.models.employee import Employee

ALLOWED_UPDATE_FIELDS = {'name': str, 'email': str,
                         'phone_number': str, 'status': str, 'service_ids': list}


class EmployeeValidation:
    """
    Validation class for Employee entities.

    Provides validation for employee creation and updates, including
    email uniqueness checks and service association validation.
    """

    @staticmethod
    def _find_employee_by_email(email: str) -> Optional['Employee']:
        """
        Search for an employee by email.

        Args:
            email (str): The email to search for.

        Returns:
            Optional[Employee]: The employee object if found, otherwise None.
        """
        return search_employee_email(email)

    @staticmethod
    def _find_employee_by_phone_number(phone_number: str) -> Optional['Employee']:
        """
        Searches for the given phone number in the employee database.

        Args:
            phone_number (str): The phone number to search for.

        Returns:
            Optional[Employee]: The employee object if found, otherwise None.
        """

        return search_employee_by_phone_number(phone_number)

    @staticmethod
    def _validate_services_exist() -> None:
        """
        Ensure at least one service exists in the system.

        Raises:
            HTTPException: If no services are registered (422).
        """
        if get_services_count() == 0:
            BaseValidation.abort_with_error(
                422, 'A service must be registered before registering an employee.', 'service')

    @staticmethod
    def _get_validated_services(service_ids: list[int]) -> list:
        """
        Validate and retrieve Service objects for the given IDs.

        Args:
            service_ids (list[int]): List of service IDs to validate.

        Returns:
            list: List of Service objects.

        Raises:
            HTTPException: If any service is not found (404).
        """
        if not service_ids:
            BaseValidation.abort_with_error(
                404, 'Service not found.', 'service')

        services = []
        for service_id in service_ids:
            service = get_service(service_id=service_id)
            if service is None:
                BaseValidation.abort_with_error(
                    404, 'Service not found.', 'service')

            services.append(service)

        return services

    @staticmethod
    def _validate_email_unique(email: str, exclude_id: Optional[int] = None) -> None:
        """
        Validate that an email is not already registered.

        Args:
            email (str): The email to check.
            exclude_id (Optional[int]): Employee ID to exclude from the check (for updates).

        Raises:
            HTTPException: If email is already registered (409).
        """
        existing = EmployeeValidation._find_employee_by_email(email)
        if existing is None:
            return

        if exclude_id is not None and getattr(existing, 'id', None) == exclude_id:
            return

        BaseValidation.abort_email_conflict()

    @staticmethod
    def validate_employee(email: str, service_ids: list[int], phone_number: str) -> list:
        """
        Validate a new employee's data.

        Args:
            email (str): The employee's email.
            service_ids (list[int]): List of service IDs to associate.

        Returns:
            list: List of validated Service objects.

        Raises:
            HTTPException: If email is taken (409), no services exist (422),
                or any service ID is invalid (404).
        """
        EmployeeValidation._validate_email_unique(email)
        EmployeeValidation._validate_services_exist()
        if EmployeeValidation._find_employee_by_phone_number(phone_number) is not None:
            BaseValidation.abort_phone_number_conflict()

        BaseValidation.validate_brazilian_phone_number(phone_number)
        return EmployeeValidation._get_validated_services(service_ids)

    @staticmethod
    def _validate_status(status: str) -> None:
        """
        Validate that the status value is one of the allowed values.

        Args:
            status (str): The status to validate.

        Raises:
            HTTPException: If status is invalid (400).
        """
        allowed_statuses = ['available', 'vacation', 'sick_leave', 'unavailable']
        if status not in allowed_statuses:
            BaseValidation.abort_with_error(
                400,
                f"Invalid status. Must be one of: {', '.join(allowed_statuses)}",
                'status'
            )


    @staticmethod
    def validate_employee_update(
        fields: dict,
        current_employee_id: Optional[int] = None
    ) -> dict:
        """
        Validate update payload and check uniqueness constraints.

        Args:
            fields (dict): Raw update payload.
            current_employee_id (Optional[int]): ID of the employee being updated. If provided,
                allows the same email if it belongs to this employee.

        Returns:
            dict: Cleaned fields ready to apply.

        Raises:
            HTTPException: For uniqueness conflicts (409) or invalid services (404).
        """
        cleaned = BaseValidation.validate_update_payload(
            fields, allowed_update_fields=ALLOWED_UPDATE_FIELDS
        )

        if 'email' in cleaned:
            EmployeeValidation._validate_email_unique(
                cleaned['email'], exclude_id=current_employee_id
            )

        if 'phone_number' in cleaned:
            existing = EmployeeValidation._find_employee_by_phone_number(cleaned['phone_number'])
            is_conflict = (
                existing is not None
                and (current_employee_id is None or
                     getattr(existing, 'id', None) != current_employee_id))

            if is_conflict:
                BaseValidation.abort_phone_number_conflict()

        if 'service_ids' in cleaned:
            cleaned['services'] = EmployeeValidation._get_validated_services(
                cleaned.pop('service_ids')
            )

        if 'status' in cleaned:
            EmployeeValidation._validate_status(cleaned['status'])

        return cleaned

"""
Business module for Employee entities.
"""

from typing import List
from business.base import get_or_404
from database.models.employee import Employee
from repositories.employee_repository import add_employee, delete_employee, get_employee, \
    update_employee
from repositories.service_repository import get_services_by_services_ids
from validations.employee_validation import EmployeeValidation


def create_employee(name: str, email: str, phone_number: str, service_ids: List[int]) -> Employee:
    """
    Creates a new Employee.

    Args:
        name (str): The employee's name.
        email (str): The employee's email.
        phone_number (str): The employee's cellphone number.
        services (List[int]): The list of services performed by the employee.

    Returns:
        Employee: Created employee.
    """

    EmployeeValidation.validate_employee(email, service_ids)

    services = get_services_by_services_ids(service_ids)

    return add_employee(name, email, phone_number, services)


def delete_employee_by_id(employee_id: int) -> bool:
    """
    Deletes an existing employee by its ID.

    Args:
        employee_id (int): The employee's unique identifier.

    Returns:
        bool: True if the employee was successfully deleted.

    Raises:
        HTTPException: If employee not found (404) or invalid ID (400).
    """

    employee = get_or_404(get_employee, employee_id, 'employee')

    return delete_employee(employee)


def update_employee_by_id(employee_id: int, **fields) -> Employee:
    """
    Updates an existing employee by its ID using keyword fields.

    Args:
        employee_id (int): The employee's unique identifier.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        Employee: Updated employee.

    Raises:
        HTTPException: If appointment not found (404) or validation fails.
    """

    employee = get_or_404(get_employee, employee_id, 'employee')

    validated = EmployeeValidation.validate_employee_update(
        fields, current_employee_id=employee_id)

    return update_employee(employee, **validated)

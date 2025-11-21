"""
Business module for Employee entities.
"""

from typing import List
from flask_smorest import abort
from database.models.employee import Employee
from repositories.employee_repository import add_employee, delete_employee, get_employee, update_employee
from repositories.service_repository import get_services_by_services_ids
from validations.employee_validation import EmployeeValidation
from validations.base import BaseValidation


def create_employee(name: str, email: str, phone_number: str, service_ids: List[int]) -> Employee:
    """
    Creates a new Employee.

    Args:
        name (str): The employee's name.
        email (str): The employee's email.
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
        werkzeug.exceptions.NotFound: If the employee does not exist.
        Exception: If an unexpected error occurs during deletion.
    """

    try:
        BaseValidation.validate_positive_int(employee_id, 'employee')

        employee = get_employee(employee_id)
        if employee is None:
            abort(404, errors={'json': ['Employee not found.']})

        return delete_employee(employee)
    except Exception as error:
        raise error


def update_employee_by_id(employee_id: int, **fields) -> Employee:
    """
    Updates an existing employee by its ID using keyword fields.

    Args:
        employee_id (int): The employee's unique identifier.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        employee: Updated employee.

    Raises:
        werkzeug.exceptions.NotFound: If the employee does not exist.
        HTTPException: If validation fails.
        Exception: If an unexpected error occurs during update.
    """

    try:
        BaseValidation.validate_positive_int(employee_id, 'employee')

        employee = get_employee(employee_id)
        if employee is None:
            abort(404, errors={'json': ['Employee not found.']})

        updates = EmployeeValidation.validate_employee_update(
            fields, current_employee_id=employee_id)

        return update_employee(employee, **updates)
    except Exception as error:
        raise error

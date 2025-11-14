"""
Business module for Employee entities.
"""

from typing import List
from flask_smorest import abort
from database.models.employee import Employee
from repositories.employee_repository import add_employee, delete_employee, get_employee
from repositories.service_repository import get_services_by_services_ids
from validations.employee_validation import EmployeeValidation
from validations.base import BaseValidation


def create_employee(name: str, email: str, services: List[int]) -> Employee:
    """
    Creates a new Employee.

    Args:
        name (str): The employee's name.
        email (str): The employee's email.
        services (List[int]): The list of services performed by the employee.

    Returns:
        Employee: Created employee.
    """

    EmployeeValidation.validate_employee(email, services)

    services = get_services_by_services_ids(services_ids=services)

    return add_employee(name, email, services)


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

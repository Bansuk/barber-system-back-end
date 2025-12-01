"""
Repository module for Employee queries.
"""

from typing import List, Optional, TYPE_CHECKING
from database.models.employee import Employee
from database.db_setup import db

if TYPE_CHECKING:
    from ..database.models.service import Service


def get_employee(employee_id: int) -> Optional[Employee]:
    """
    Retrieves an employee by its ID.

    Args:
        employee_id (int): The employee id to search.

    Returns:
        Optional[Employee]: The employee found or None.
    """

    return db.session.query(Employee).filter_by(id=employee_id).first()


def search_employee_email(email: str) -> Optional[str]:
    """
    Retrieves an employee email.

    Args:
        email (str): The employee email to search.

    Returns:
        Optional[str]: The email found or None.
    """

    return db.session.query(Employee.email).filter_by(email=email).first()


def search_employee_by_phone_number(phone_number: str) -> Optional[Employee]:
    """
    Retrieves a employee by phone number.

    Args:
        phone_number (str): The employee's phone number to search.

    Returns:
        Optional[Employee]: The matching employee or None.
    """

    return Employee.query.filter_by(phone_number=phone_number).first()


def get_all_employees() -> List[Employee]:
    """
    Retrieves all registered employees.

    Returns:
        List[Employee]: A list of registered employees.
    """

    return db.session.query(Employee).all()


def delete_employee(employee: Employee) -> bool:
    """
    Deletes the given employee from the database.

    Returns:
        bool: True if the employee was deleted successfully.

    Raises:
        Exception: If the deletion fails.
    """

    try:
        db.session.delete(employee)
        db.session.commit()

        return True
    except Exception as error:
        db.session.rollback()
        raise error


def add_employee(name: str, email: str, phone_number: str, services: List['Service']) -> Employee:
    """
    Adds a new employee to the database.

    Returns:
        Employee: Created employee.

    Raises:
        Exception: If the addition fails.
    """

    try:
        employee = Employee(name, email, phone_number,
                            services, appointments=[])
        db.session.add(employee)
        db.session.commit()

        return employee
    except Exception as error:
        db.session.rollback()
        raise error


def update_employee(employee: Employee, **fields) -> Employee:
    """
    Updates an existing employee in the database.

    Returns:
        Employee: Updated employee.

    Raises:
        Exception: If the update fails.
    """

    try:
        for key, value in fields.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)

        db.session.add(employee)
        db.session.commit()

        return employee
    except Exception as error:
        db.session.rollback()
        raise error

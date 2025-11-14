"""
Repository module for Employee queries.
"""

from typing import List, Optional
from database.models.employee import Employee
from database.db_setup import db


def get_employee(employee_id: int) -> Optional[Employee]:
    """
    Retrieves an employee by its ID.

    Args:
        employee_id (int): The employee id to search.

    Returns:
        Employee: The employee found or None.
    """

    return db.session.query(Employee).filter_by(id=employee_id).first()


def search_employee_email(email: str) -> Optional[str]:
    """
    Retrieves an employee email.

    Args:
        email (str): The employee email to search.

    Returns:
        str: The email found or None.
    """

    return db.session.query(Employee.email).filter_by(email=email).first()


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

"""
Repository module for Employee queries.
"""

from typing import List, Optional, TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
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


def search_employee_email(email: str) -> Optional[Employee]:
    """
    Retrieves an employee by email.

    Args:
        email (str): The employee email to search.

    Returns:
        Optional[Employee]: The employee found or None.
    """

    return db.session.query(Employee).filter_by(email=email).first()


def search_employee_by_phone_number(phone_number: str) -> Optional[Employee]:
    """
    Retrieves a employee by phone number.

    Args:
        phone_number (str): The employee's phone number to search.

    Returns:
        Optional[Employee]: The matching employee or None.
    """

    return db.session.query(Employee).filter_by(phone_number=phone_number).first()


def get_all_employees(status: Optional[str] = None) -> List[Employee]:
    """
    Retrieves all registered employees.

    Args:
        status (Optional[str]): Filter employees by status. If None, counts all employees.

    Returns:
        List[Employee]: A list of registered employees.
    """

    query = db.session.query(Employee)

    if status is not None:
        query = query.filter_by(status=status)

    return query.all()


def count_employees(status: Optional[str] = None) -> int:
    """
    Counts the total number of registered employees.

    Args:
        status (Optional[str]): Filter employees by status. If None, counts all employees.

    Returns:
        int: The total count of employees.
    """

    query = db.session.query(Employee)

    if status is not None:
        query = query.filter_by(status=status)

    return query.count()


def delete_employee(employee: Employee) -> bool:
    """
    Deletes the given employee from the database.

    Args:
        employee (Employee): The employee to delete.

    Returns:
        bool: True if the employee was deleted successfully.

    Raises:
        SQLAlchemyError: If the deletion fails.
    """

    try:
        db.session.delete(employee)
        db.session.commit()

        return True
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def add_employee(name: str, email: str, phone_number: str, services: List['Service'], status: str = 'available') -> Employee:
    """
    Adds a new employee to the database.

    Args:
        name (str): The employee's name.
        email (str): The employee's email.
        phone_number (str): The employee's phone number.
        services (List[Service]): List of services the employee can perform.
        status (str): The employee's availability status.

    Returns:
        Employee: Created employee.

    Raises:
        SQLAlchemyError: If the addition fails.
    """

    try:
        employee = Employee(name, email, phone_number,
                            services, appointments=[], status=status)
        db.session.add(employee)
        db.session.commit()

        return employee
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def update_employee(employee: Employee, **fields) -> Employee:
    """
    Updates an existing employee in the database.

    Args:
        employee (Employee): The employee to update.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        Employee: Updated employee.

    Raises:
        SQLAlchemyError: If the update fails.
    """

    try:
        for key, value in fields.items():
            if hasattr(employee, key) and value is not None:
                setattr(employee, key, value)

        db.session.add(employee)
        db.session.commit()

        return employee
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error

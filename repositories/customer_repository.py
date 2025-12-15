"""
Repository module for Customer queries.
"""

from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from database.models.customer import Customer
from database.db_setup import db


def get_customer(customer_id: int) -> Optional[Customer]:
    """
    Retrieves a customer by its ID.

    Args:
        customer_id (int): The customer's ID.

    Returns:
        Optional[Customer] | None: The customer found or None.
    """

    return db.session.query(Customer).filter_by(id=customer_id).first()


def search_customer_by_email(email: str) -> Optional[Customer]:
    """
    Retrieves a customer by email.

    Args:
        email (str): The customer's email to search.

    Returns:
        Optional[Customer] | None: The matching customer or None.
    """

    return db.session.query(Customer).filter_by(email=email).first()


def search_customer_by_phone_number(phone_number: str) -> Optional[Customer]:
    """
    Retrieves a customer by phone number.

    Args:
        phone_number (str): The customer's phone number to search.

    Returns:
        Optional[Customer] | None: The matching customer or None.
    """

    return db.session.query(Customer).filter_by(phone_number=phone_number).first()


def get_all_customers() -> List[Customer]:
    """
    Retrieves all registered customers.

    Returns:
        List[Customer]: A list of registered customers.
    """

    return db.session.query(Customer).all()


def count_customers() -> int:
    """
    Counts the total number of registered customers.

    Returns:
        int: The total count of customers.
    """

    return db.session.query(Customer).count()


def delete_customer(customer: Customer) -> bool:
    """
    Deletes the given customer from the database.

    Args:
        customer (Customer): The customer to delete.

    Returns:
        bool: True if the customer was deleted successfully.

    Raises:
        SQLAlchemyError: If the deletion fails.
    """

    try:
        db.session.delete(customer)
        db.session.commit()

        return True
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def add_customer(name: str, email: str, phone_number: str) -> Customer:
    """
    Adds a new customer to the database.

    Args:
        name (str): The customer's name.
        email (str): The customer's email.
        phone_number (str): The customer's phone number.

    Returns:
        Customer: Created customer.

    Raises:
        SQLAlchemyError: If the addition fails.
    """

    try:
        customer = Customer(name, email, phone_number, appointments=[])

        db.session.add(customer)
        db.session.commit()

        return customer
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error


def update_customer(customer: Customer, **fields) -> Customer:
    """
    Updates an existing customer in the database.

    Args:
        customer (Customer): The customer to update.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        Customer: Updated customer.

    Raises:
        SQLAlchemyError: If the update fails.
    """

    try:
        for key, value in fields.items():
            if hasattr(customer, key) and value is not None:
                setattr(customer, key, value)

        db.session.add(customer)
        db.session.commit()

        return customer
    except SQLAlchemyError as error:
        db.session.rollback()
        raise error

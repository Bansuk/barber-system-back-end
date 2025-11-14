"""
Repository module for Customer queries.
"""

from typing import List, Optional
from database.models.customer import Customer
from database.db_setup import db


def get_customer(customer_id: int) -> Optional[Customer]:
    """
    Retrieves a customer by its ID.

    Args:
        customer_id (int): The customer's ID.

    Returns:
        Customer: The customer found or None.
    """

    return db.session.query(Customer).filter_by(id=customer_id).first()


def search_customer_email(email: str) -> Optional[str]:
    """
    Retrieves a customer email.

    Args:
        email (str): The customer's email to search.

    Returns:
        str: The email found or None.
    """

    return db.session.query(Customer.email).filter_by(email=email).first()


def get_all_customers() -> List[Customer]:
    """
    Retrieves all registered customers.

    Returns:
        List[Customer]: A list of registered customers.
    """

    return db.session.query(Customer).all()


def delete_customer(customer: Customer) -> bool:
    """
    Deletes the given customer from the database.

    Returns:
        bool: True if the customer was deleted successfully.

    Raises:
        Exception: If the deletion fails.
    """

    try:
        db.session.delete(customer)
        db.session.commit()

        return True
    except Exception as error:
        db.session.rollback()
        raise error

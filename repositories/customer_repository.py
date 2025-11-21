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


def search_customer_by_email(email: str) -> Optional[Customer]:
    """
    Retrieves a customer by email.

    Args:
        email (str): The customer's email to search.

    Returns:
        Customer | None: The matching customer or None.
    """

    return Customer.query.filter_by(email=email).first()


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


def add_customer(name: str, email: str, phone_number: str) -> Customer:
    """
    Adds a new customer to the database.

    Returns:
        Customer: Created customer.

    Raises:
        Exception: If the addition fails.
    """

    try:
        customer = Customer(name, email, phone_number, appointments=[])

        db.session.add(customer)
        db.session.commit()

        return customer
    except Exception as error:
        db.session.rollback()
        raise error


def update_customer(customer: Customer, **fields) -> Customer:
    """
    Updates an existing customer in the database.

    Returns:
        Customer: Updated customer.

    Raises:
        Exception: If the update fails.
    """

    try:
        for key, value in fields.items():
            if hasattr(customer, key) and value is not None:
                setattr(customer, key, value)

        db.session.add(customer)
        db.session.commit()

        return customer
    except Exception as error:
        db.session.rollback()
        raise error

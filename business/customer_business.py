"""
Business module for Customer entities.
"""

from flask_smorest import abort
from repositories.customer_repository import delete_customer, get_customer
from database.models.customer import Customer
from database.db_setup import db
from validations.customer_validation import CustomerValidation


def create_customer(name: str, email: str) -> Customer:
    """
    Creates a new customer.

    Args:
        name (str): The customer's name.
        email (str): The customer's email.

    Returns:
        Customer: Created customer.
    """

    CustomerValidation.validate_customer(email)

    customer = Customer(name, email, appointments=[])

    try:
        db.session.add(customer)
        db.session.commit()

        return customer
    except Exception as error:
        db.session.rollback()
        raise error


def delete_customer_by_id(customer_id: int) -> bool:
    """
    Deletes an existing customer by its ID.

    Args:
        customer_id (int): The customer's unique identifier.

    Returns:
        bool: True if the customer was successfully deleted.

    Raises:
        werkzeug.exceptions.NotFound: If the customer does not exist.
        Exception: If an unexpected error occurs during deletion.
    """

    try:
        CustomerValidation.validate_customer_id_type(customer_id)

        customer = get_customer(customer_id)
        if customer is None:
            abort(404, errors={'json': ['Customer not found.']})

        return delete_customer(customer)
    except Exception as error:
        raise error

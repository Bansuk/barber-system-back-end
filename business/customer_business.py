"""
Business module for Customer entities.
"""

from flask_smorest import abort
from repositories.customer_repository import add_customer, delete_customer, get_customer
from database.models.customer import Customer
from validations.base import BaseValidation
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

    return add_customer(name, email)


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
        BaseValidation.validate_positive_int(customer_id, 'customer')

        customer = get_customer(customer_id)
        if customer is None:
            abort(404, errors={'json': ['Customer not found.']})

        return delete_customer(customer)
    except Exception as error:
        raise error

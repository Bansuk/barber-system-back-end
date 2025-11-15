"""
Business module for Customer entities.
"""

from flask_smorest import abort
from validations.customer_validation import CustomerValidation
from validations.base import BaseValidation
from database.models.customer import Customer
from repositories.customer_repository import (
    add_customer,
    delete_customer,
    get_customer,
    update_customer,
)


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


def update_customer_by_id(customer_id: int, **fields) -> Customer:
    """
    Updates an existing customer by its ID using keyword fields.

    Args:
        customer_id (int): The customer's unique identifier.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        Customer: Updated customer.

    Raises:
        werkzeug.exceptions.NotFound: If the customer does not exist.
        HTTPException: If validation fails.
        Exception: If an unexpected error occurs during update.
    """

    try:
        BaseValidation.validate_positive_int(customer_id, 'customer')

        customer = get_customer(customer_id)
        if customer is None:
            abort(404, errors={'json': ['Customer not found.']})

        updates = CustomerValidation.validate_customer_update(
            fields, current_customer_id=customer_id)

        return update_customer(customer, **updates)
    except Exception as error:
        raise error

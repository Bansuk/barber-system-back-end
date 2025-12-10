"""
Business module for Customer entities.
"""

from datetime import datetime
from business.base import get_or_404
from database.models.customer import Customer
from repositories.customer_repository import (
    add_customer,
    delete_customer,
    get_customer,
    update_customer,
)
from validations.base import BaseValidation
from validations.customer_validation import CustomerValidation


def create_customer(name: str, email: str, phone_number: str) -> Customer:
    """
    Creates a new customer.

    Args:
        name (str): The customer's name.
        email (str): The customer's email.
        phone_number (str): The customer's cellphone number.

    Returns:
        Customer: Created customer.
    """

    CustomerValidation.validate_customer(email, phone_number)

    return add_customer(name, email, phone_number)


def get_customer_by_id(customer_id: int) -> Customer:
    """
    Retrieves a customer by its ID.

    Args:
        customer_id (int): The customer's unique identifier.

    Returns:
        Customer: The customer found.

    Raises:
        HTTPException: If customer not found (404) or invalid ID (400).
    """

    return get_or_404(get_customer, customer_id, 'customer')


def delete_customer_by_id(customer_id: int) -> bool:
    """
    Deletes an existing customer by its ID.

    Args:
        customer_id (int): The customer's unique identifier.

    Returns:
        bool: True if the customer was successfully deleted.

    Raises:
        HTTPException: If customer not found (404), invalid ID (400), or customer has future appointments (409).
    """

    customer = get_or_404(get_customer, customer_id, 'customer')

    future_appointments = [apt for apt in customer.appointments if apt.date > datetime.now()]
    if future_appointments:
        BaseValidation.abort_with_error(
            409, 
            f"Cannot delete customer. It has {len(future_appointments)} future appointment(s).",
            'customer'
        )

    return delete_customer(customer)


def update_customer_by_id(customer_id: int, **fields) -> Customer:
    """
    Updates an existing customer by its ID using keyword fields.

    Args:
        customer_id (int): The customer's unique identifier.
        **fields: Arbitrary keyword arguments representing fields to update.

    Returns:
        Customer: Updated customer.

    Raises:
        HTTPException: If customer not found (404) or validation fails.
    """

    customer = get_or_404(get_customer, customer_id, 'customer')

    validated = CustomerValidation.validate_customer_update(
        fields, current_customer_id=customer_id)

    return update_customer(customer, **validated)

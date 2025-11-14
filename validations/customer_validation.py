"""
Validation module for Customer entities.
"""

from flask_smorest import abort
from repositories.customer_repository import search_customer_email


class CustomerValidation():
    """
    Validation class for Customer entities.
    """

    @staticmethod
    def _email_exists(email: str) -> bool:
        """
        Checks if the given email is already registered in the Customer database.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if the email exists, False otherwise.
        """

        return search_customer_email(email) is not None

    @staticmethod
    def validate_customer(email: str) -> None:
        """
        Validates customer.

        Args:
            email (str): The customer's email.

        Raises:
            HTTPException: If any validation fails.
        """

        if CustomerValidation._email_exists(email):
            abort(409, errors={
                'json': {
                    'email': ['Email already registered.']
                }
            })

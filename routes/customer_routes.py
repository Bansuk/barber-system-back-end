"""
Route module for Customer routes.
"""

from flask_smorest import Blueprint as SmorestBlueprint
from schemas.customer_schema import CustomerSchema, CustomerViewSchema
from business.customer_business import create_customer, delete_customer_by_id, get_customer_by_id, update_customer_by_id
from repositories.customer_repository import count_customers, get_all_customers
from routes.docs.customer_doc import (
    DELETE_CUSTOMER_DESCRIPTION,
    DELETE_CUSTOMER_SUMMARY,
    GET_CUSTOMER_BY_ID_DESCRIPTION,
    GET_CUSTOMER_BY_ID_SUMMARY,
    GET_CUSTOMER_COUNT_DESCRIPTION,
    GET_CUSTOMER_COUNT_SUMMARY,
    GET_CUSTOMER_DESCRIPTION,
    GET_CUSTOMER_SUMMARY,
    POST_CUSTOMER_DESCRIPTION,
    POST_CUSTOMER_SUMMARY,
    UPDATE_CUSTOMER_DESCRIPTION,
    UPDATE_CUSTOMER_SUMMARY,
    delete_customer_responses,
    get_customer_by_id_responses,
    post_customer_responses,
    update_customer_responses,
)

customer_bp = SmorestBlueprint(
    'Customer', __name__, description='Operações em Clientes')


@customer_bp.route('/customer', methods=['POST'])
@customer_bp.arguments(CustomerSchema)
@customer_bp.response(201, CustomerViewSchema, description='Cliente cadastrado com sucesso.')
@customer_bp.doc(summary=POST_CUSTOMER_SUMMARY, description=POST_CUSTOMER_DESCRIPTION,
                 responses=post_customer_responses)
def add_customer(customer_data):
    """
    Handles the creation of a new customer.

    This endpoint processes a form submission (JSON) to create a new customer record.

    Receives a JSON payload with 'name', 'email', 'phone_number',
    calls the business logic to create a customer,
    and returns an appropriate response.

    Returns:
        JSON response:
        - 201 (Created): Customer created successfully.
        - 400 (Bad Request): Invalid body JSON format.
        - 409 (Conflict): Email already registered.
        - 422 (Unprocessable Entity): Validation error.
    """

    return create_customer(**customer_data)


@customer_bp.route('/customers', methods=['GET'])
@customer_bp.response(200, CustomerViewSchema(many=True))
@customer_bp.doc(summary=GET_CUSTOMER_SUMMARY, description=GET_CUSTOMER_DESCRIPTION)
def get_customers():
    """
    Retrieve a list of all customers.

    This endpoint returns a collection of customer records in JSON format.

    Responses:         
        JSON response:
        - 200 (OK): Successfully retrieved the list of customers.                                                     
    """

    return get_all_customers()


@customer_bp.route('/customer/<int:customer_id>', methods=['GET'])
@customer_bp.response(200, CustomerViewSchema)
@customer_bp.doc(summary=GET_CUSTOMER_BY_ID_SUMMARY, description=GET_CUSTOMER_BY_ID_DESCRIPTION, responses=get_customer_by_id_responses)
def get_customer(customer_id):
    """
    Retrieve a single customer by ID.

    This endpoint returns a specific customer record in JSON format.

    Responses:
        JSON response:
        - 200 (OK): Successfully retrieved the customer.
        - 404 (Not Found): Customer was not found.
    """

    return get_customer_by_id(customer_id)


@customer_bp.route('/customers/count', methods=['GET'])
@customer_bp.response(200)
@customer_bp.doc(summary=GET_CUSTOMER_COUNT_SUMMARY, description=GET_CUSTOMER_COUNT_DESCRIPTION)
def get_customer_count():
    """
    Retrieve the total number of customers.

    This endpoint returns the count of all registered customers.

    Responses:
        JSON response:
        - 200 (OK): Successfully retrieved the customer count.
    """

    return count_customers()


@customer_bp.route('/customer/<int:customer_id>', methods=['DELETE'])
@customer_bp.response(204)
@customer_bp.doc(summary=DELETE_CUSTOMER_SUMMARY, description=DELETE_CUSTOMER_DESCRIPTION, responses=delete_customer_responses)
def remove_customer(customer_id):
    """
    Deletes a customer.

    Responses:
        JSON response:
        - 204 (No Content): Successfully deleted the customer.
        - 400 (Bad Request): Invalid ID format.
        - 404 (Not Found): Customer was not found.
    """
    return delete_customer_by_id(customer_id)


@customer_bp.route('/customer/<int:customer_id>', methods=['PATCH'])
@customer_bp.arguments(CustomerSchema(partial=True))
@customer_bp.response(200, CustomerViewSchema)
@customer_bp.doc(summary=UPDATE_CUSTOMER_SUMMARY, description=UPDATE_CUSTOMER_DESCRIPTION, responses=update_customer_responses)
def update_customer(customer_data, customer_id):
    """
    Partially updates a customer.

    Responses:
        JSON response:
        - 200 (OK): Successfully updated the customer.
        - 400 (Bad Request): Invalid fields.
        - 404 (Not Found): Customer was not found.
        - 409 (Conflict): Email already registered.
    """

    return update_customer_by_id(customer_id, **customer_data)

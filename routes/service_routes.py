"""
Route module for Service routes.
"""

from flask import request
from flask_smorest import Blueprint as SmorestBlueprint
from schemas.service_schema import ServiceSchema, ServiceViewSchema
from business.service_business import create_service, delete_service_by_id, \
    get_service_by_id, update_service_by_id
from repositories.service_repository import get_all_services, get_services_count
from routes.docs.service_doc import (
    DELETE_SERVICE_DESCRIPTION,
    DELETE_SERVICE_SUMMARY,
    GET_SERVICE_DESCRIPTION,
    GET_SERVICE_SUMMARY,
    GET_SERVICE_BY_ID_DESCRIPTION,
    GET_SERVICE_BY_ID_SUMMARY,
    GET_SERVICE_COUNT_DESCRIPTION,
    GET_SERVICE_COUNT_SUMMARY,
    POST_SERVICE_DESCRIPTION,
    POST_SERVICE_SUMMARY,
    UPDATE_SERVICE_DESCRIPTION,
    UPDATE_SERVICE_SUMMARY,
    delete_service_responses,
    get_service_by_id_responses,
    post_service_responses,
    update_service_responses
)


service_bp = SmorestBlueprint(
    'Service', __name__, description='Operações em Serviços')


@service_bp.route('/service', methods=['POST'])
@service_bp.arguments(ServiceSchema)
@service_bp.response(201, ServiceViewSchema, description='Serviço cadastrado com sucesso.')
@service_bp.doc(summary=POST_SERVICE_SUMMARY, description=POST_SERVICE_DESCRIPTION,
                responses=post_service_responses)
def add_service(service_data):
    """
    Handles the creation of a new service.

    This endpoint processes a form submission (JSON) to create a new service record.

    Receives a JSON payload with 'name' and 'price',
    calls the business logic to create a service,
    and returns an appropriate response.

    Returns:
        JSON response:
        - 201 (Created): Service created successfully.
        - 400 (Bad Request): Invalid body JSON format.
        - 409 (Conflict): Service already registered.
        - 422 (Unprocessable Entity): Validation error.
    """

    return create_service(**service_data)


@service_bp.route('/services', methods=['GET'])
@service_bp.response(200, ServiceViewSchema(many=True))
@service_bp.doc(summary=GET_SERVICE_SUMMARY, description=GET_SERVICE_DESCRIPTION)
def get_services():
    """
    Retrieve a list of all services.

    This endpoint returns a collection of services records in JSON format.

    Responses:         
        JSON response:
        - 200 (OK): Successfully retrieved the list of services.                                                     
    """

    return get_all_services()


@service_bp.route('/service/<int:service_id>', methods=['GET'])
@service_bp.response(200, ServiceViewSchema)
@service_bp.doc(summary=GET_SERVICE_BY_ID_SUMMARY, description=GET_SERVICE_BY_ID_DESCRIPTION, responses=get_service_by_id_responses)
def get_service(service_id):
    """
    Retrieve a single service by ID.

    This endpoint returns a specific service record in JSON format.

    Responses:
        JSON response:
        - 200 (OK): Successfully retrieved the service.
        - 404 (Not Found): service was not found.
    """

    return get_service_by_id(service_id)


@service_bp.route('/services/count', methods=['GET'])
@service_bp.response(200)
@service_bp.doc(
    summary=GET_SERVICE_COUNT_SUMMARY,
    description=GET_SERVICE_COUNT_DESCRIPTION,
    parameters=[{
        'name': 'status',
        'in': 'query',
        'schema': {'type': 'string', 'enum': ['available', 'unavailable']},
        'required': False,
        'description': 'Filtra serviços pelo status: available (disponíveis) '
        'ou unavailable (indisponíveis)'
    }]
)
def get_service_count():
    """
    Retrieve the total number of services.

    This endpoint returns the count of all registered services.
    Accepts optional query parameter 'status' with values: 'available' or 'unavailable'.

    Query Parameters:
        status (str, optional): Filter services by status.
            - 'available': Available services
            - 'unavailable': Unavailable services
            - omitted: All services

    Responses:
        JSON response:
        - 200 (OK): Successfully retrieved the service count.
    """

    status = request.args.get('status')

    return get_services_count(status)


@service_bp.route('/service/<int:service_id>', methods=['DELETE'])
@service_bp.response(204)
@service_bp.doc(summary=DELETE_SERVICE_SUMMARY, description=DELETE_SERVICE_DESCRIPTION, responses=delete_service_responses)
def remove_service(service_id):
    """
    Deletes a service.

    Responses:
        JSON response:
        - 204 (No Content): Successfully deleted the service.
        - 400 (Bad Request): Invalid ID format.
        - 404 (Not Found): service was not found.
        - 409 (Conflict): Service is associated with employees or has future appointments.
    """
    return delete_service_by_id(service_id)


@service_bp.route('/service/<int:service_id>', methods=['PATCH'])
@service_bp.arguments(ServiceSchema(partial=True))
@service_bp.response(200, ServiceViewSchema)
@service_bp.doc(summary=UPDATE_SERVICE_SUMMARY, description=UPDATE_SERVICE_DESCRIPTION, responses=update_service_responses)
def update_service(service_data, service_id):
    """
    Partially updates a service.

    Responses:
        JSON response:
        - 200 (OK): Successfully updated the service.
        - 400 (Bad Request): Invalid fields.
        - 404 (Not Found): Service was not found.
        - 409 (Conflict): Service already registered.
        - 422 (Unprocessable Entity): Validation error.
    """

    return update_service_by_id(service_id, **service_data)

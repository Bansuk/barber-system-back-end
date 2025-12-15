"""
Route module for Employee routes.
"""

from flask import request
from flask_smorest import Blueprint as SmorestBlueprint
from schemas.employee_schema import EmployeeSchema, EmployeeViewSchema
from business.employee_business import create_employee, delete_employee_by_id, update_employee_by_id
from repositories.employee_repository import count_employees, get_all_employees
from routes.docs.employee_doc import (
    DELETE_EMPLOYEE_DESCRIPTION,
    DELETE_EMPLOYEE_SUMMARY,
    GET_EMPLOYEE_COUNT_DESCRIPTION,
    GET_EMPLOYEE_COUNT_SUMMARY,
    GET_EMPLOYEE_DESCRIPTION,
    GET_EMPLOYEE_SUMMARY,
    POST_EMPLOYEE_DESCRIPTION,
    POST_EMPLOYEE_SUMMARY,
    UPDATE_EMPLOYEE_DESCRIPTION,
    UPDATE_EMPLOYEE_SUMMARY,
    delete_employee_responses,
    post_employee_responses,
    update_employee_responses,
)

employee_bp = SmorestBlueprint(
    'Employee', __name__, description='Operações em Funcionários')


@employee_bp.route('/employee', methods=['POST'])
@employee_bp.arguments(EmployeeSchema)
@employee_bp.doc(summary=POST_EMPLOYEE_SUMMARY, description=POST_EMPLOYEE_DESCRIPTION,
                 responses=post_employee_responses)
@employee_bp.response(201, EmployeeViewSchema, description='Funcionário(a) cadastrado com sucesso.')
def add_employee(employee_data):
    """
    Handles the creation of a new employee.

    This endpoint processes a form submission (JSON) to create a new employee record.

    Receives a JSON payload with 'name', 'email', 'phone_number' and 
    'services', calls the business logic to create a 
    employee, and returns an appropriate response.

    Returns:
        JSON response:
        - 201 (Created): Employee created successfully.
        - 400 (Bad Request): Invalid body JSON format.
        - 404 (Not Found): Service not found.
        - 409 (Conflict): Email already registered.
        - 422 (Unprocessable Entity): Validation error.
    """

    return create_employee(**employee_data)


@employee_bp.route('/employees', methods=['GET'])
@employee_bp.response(200, EmployeeViewSchema(many=True))
@employee_bp.doc(
    summary=GET_EMPLOYEE_SUMMARY,
    description=GET_EMPLOYEE_DESCRIPTION,
    parameters=[{
        'name': 'status',
        'in': 'query',
        'schema': {
            'type': 'string',
            'enum': ['available', 'vacation', 'sick_leave', 'unavailable']
        },
        'required': False,
        'description': 'Filtra funcionários(as) pelo status: available (disponíveis), '
        'vacation (férias), sick_leave (licença médica) ou unavailable (indisponíveis)'
    }]
)
def get_employees():
    """
    Retrieves a list of all employees.
    Optionally filter by status using query parameter.

    Query Parameters:
        status (str, optional): Filter employees by status 
                               (available, vacation, sick_leave, unavailable)

    Returns:
        JSON response:
        - 200 (OK): List of employees retrieved successfully.
    """

    status = request.args.get('status', None)

    return get_all_employees(status)


@employee_bp.route('/employees/count', methods=['GET'])
@employee_bp.response(200)
@employee_bp.doc(
    summary=GET_EMPLOYEE_COUNT_SUMMARY,
    description=GET_EMPLOYEE_COUNT_DESCRIPTION,
    parameters=[{
        'name': 'status',
        'in': 'query',
        'schema': {
            'type': 'string',
            'enum': ['available', 'vacation', 'sick_leave', 'unavailable']
        },
        'required': False,
        'description': 'Filtra funcionários(as) pelo status: available (disponíveis), '
        'vacation (férias), sick_leave (licença médica) ou unavailable (indisponíveis)'
    }]
)
def get_employee_count():
    """
    Retrieve the total number of employees.

    This endpoint returns the count of all registered employees.
    Optionally filter by status using query parameter.

    Query Parameters:
        status (str, optional): Filter employees by status 
                               (available, vacation, sick_leave, unavailable)

    Responses:
        JSON response:
        - 200 (OK): Successfully retrieved the employee count.
    """

    status = request.args.get('status', None)

    return count_employees(status=status)


@employee_bp.route('/employee/<int:employee_id>', methods=['DELETE'])
@employee_bp.response(204)
@employee_bp.doc(summary=DELETE_EMPLOYEE_SUMMARY, description=DELETE_EMPLOYEE_DESCRIPTION, responses=delete_employee_responses)
def remove_employee(employee_id):
    """
    Deletes an employee.

    Responses:
        JSON response:
        - 204 (No Content): Successfully deleted the employee.
        - 400 (Bad Request): Invalid ID format.
        - 404 (Not Found): Employee was not found.
    """
    return delete_employee_by_id(employee_id)


@employee_bp.route('/employee/<int:employee_id>', methods=['PATCH'])
@employee_bp.arguments(EmployeeSchema(partial=True))
@employee_bp.response(200, EmployeeViewSchema)
@employee_bp.doc(summary=UPDATE_EMPLOYEE_SUMMARY, description=UPDATE_EMPLOYEE_DESCRIPTION, responses=update_employee_responses)
def update_employee(employee_data, employee_id):
    """
    Partially updates a employee.

    Responses:
        JSON response:
        - 200 (OK): Successfully updated the employee.
        - 400 (Bad Request): Invalid fields.
        - 404 (Not Found): Employee was not found.
        - 409 (Conflict): Email already registered.
        - 422 (Unprocessable Entity): Validation error.
    """

    return update_employee_by_id(employee_id, **employee_data)

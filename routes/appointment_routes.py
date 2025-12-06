"""
Route module for Appointment routes.
"""

from flask_smorest import Blueprint as SmorestBlueprint
from schemas.appointment_schema import AppointmentSchema, AppointmentViewSchema
from business.appointment_business import create_appointment, delete_appointment_by_id,  \
    update_appointment_by_id
from repositories.appointment_repository import get_all_appointments, get_appointments_count
from routes.docs.appointment_doc import (
    DELETE_APPOINTMENT_DESCRIPTION,
    DELETE_APPOINTMENT_SUMMARY,
    GET_APPOINTMENT_COUNT_DESCRIPTION,
    GET_APPOINTMENT_COUNT_SUMMARY,
    GET_APPOINTMENT_DESCRIPTION,
    GET_APPOINTMENT_SUMMARY,
    POST_APPOINTMENT_DESCRIPTION,
    POST_APPOINTMENT_SUMMARY,
    UPDATE_APPOINTMENT_DESCRIPTION,
    UPDATE_APPOINTMENT_SUMMARY,
    delete_appointment_responses,
    post_appointment_responses,
    update_appointment_responses
)

appointment_bp = SmorestBlueprint(
    'Appointment', __name__, description='Operações em Agendamentos')


@appointment_bp.route('/appointment', methods=['POST'])
@appointment_bp.arguments(AppointmentSchema)
@appointment_bp.response(201, AppointmentViewSchema, description='Agendamento realizado com sucesso.')
@appointment_bp.doc(summary=POST_APPOINTMENT_SUMMARY, description=POST_APPOINTMENT_DESCRIPTION,
                    responses=post_appointment_responses)
def add_appointment(apointment_data):
    """
    Handles the creation of a new appointment.

    This endpoint processes a form submission (JSON) to create a new appointment record.

    Receives a JSON payload with 'date', 'customer_id', 'employee_id', and 'appointments_ids',
    calls the business logic to create an appointment,
    and returns an appropriate response.

    Returns:
        JSON response:
        - 201 (Created): Appointment created successfully.
        - 400 (Bad Request): Invalid body JSON format/Invalid date.
        - 404 (Not Found): Provided value was not found.
        - 409 (Conflict): Date already booked.
        - 422 (Unprocessable Entity): Validation error.
    """

    return create_appointment(**apointment_data)


@appointment_bp.route('/appointments', methods=['GET'])
@appointment_bp.response(200, AppointmentViewSchema(many=True))
@appointment_bp.doc(summary=GET_APPOINTMENT_SUMMARY, description=GET_APPOINTMENT_DESCRIPTION)
def get_appointments():
    """
    Retrieves a list of all appointments.

    This endpoint returns a collection of appointments records in JSON format.

    Responses:         
        JSON response:
        - 200 (OK): Successfully retrieved the list of appointments.
    """

    return get_all_appointments()


@appointment_bp.route('/appointments/count', methods=['GET'])
@appointment_bp.response(200)
@appointment_bp.doc(
    summary=GET_APPOINTMENT_COUNT_SUMMARY, 
    description=GET_APPOINTMENT_COUNT_DESCRIPTION,
    parameters=[{
        'name': 'period',
        'in': 'query',
        'schema': {'type': 'string', 'enum': ['all', 'past', 'upcoming'], 'default': 'all'},
        'required': False,
        'description': 'Filter appointments by time period: all (todos), past (passados), or upcoming (próximos)'
    }]
)
def get_appointment_count():
    """
    Retrieve the total number of appointments.

    This endpoint returns the count of all registered appointments.
    Accepts optional query parameter 'period' with values: 'all', 'past', or 'upcoming'.

    Query Parameters:
        period (str, optional): Filter appointments by time period.
            - 'all' or omitted: All appointments
            - 'past': Appointments before current time
            - 'upcoming': Appointments from current time onwards

    Responses:
        JSON response:
        - 200 (OK): Successfully retrieved the appointment count.
    """
    from flask import request
    
    period = request.args.get('period', 'all')
    
    return get_appointments_count(period)


@appointment_bp.route('/appointment/<int:appointment_id>', methods=['DELETE'])
@appointment_bp.response(204)
@appointment_bp.doc(summary=DELETE_APPOINTMENT_SUMMARY, description=DELETE_APPOINTMENT_DESCRIPTION, responses=delete_appointment_responses)
def remove_appointment(appointment_id):
    """
    Deletes a appointment.

    Responses:
        JSON response:
        - 204 (No Content): Successfully deleted the appointment.
        - 400 (Bad Request): Invalid ID format.
        - 404 (Not Found): Appointment was not found.
    """
    return delete_appointment_by_id(appointment_id)


@appointment_bp.route('/appointment/<int:appointment_id>', methods=['PATCH'])
@appointment_bp.arguments(AppointmentSchema(partial=True))
@appointment_bp.response(200, AppointmentViewSchema)
@appointment_bp.doc(summary=UPDATE_APPOINTMENT_SUMMARY, description=UPDATE_APPOINTMENT_DESCRIPTION, responses=update_appointment_responses)
def update_appointment(appointment_data, appointment_id):
    """
    Partially updates a appointment.

    Responses:
        JSON response:
        - 200 (OK): Successfully updated the appointment.
        - 400 (Bad Request): Invalid fields.
        - 404 (Not Found): Appointment was not found.
        - 409 (Conflict): Appointment already registered.
    """

    return update_appointment_by_id(appointment_id, **appointment_data)

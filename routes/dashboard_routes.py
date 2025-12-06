"""
Route module for Dashboard routes.
"""

from flask_smorest import Blueprint as SmorestBlueprint
from repositories.customer_repository import count_customers
from repositories.employee_repository import count_employees
from repositories.service_repository import get_services_count
from repositories.appointment_repository import get_appointments_count
from routes.docs.dashboard_doc import (
    GET_DASHBOARD_STATS_DESCRIPTION,
    GET_DASHBOARD_STATS_SUMMARY
)

dashboard_bp = SmorestBlueprint(
    'Dashboard', __name__, description='Operações de Dashboard')


@dashboard_bp.route('/dashboard/stats', methods=['GET'])
@dashboard_bp.response(200)
@dashboard_bp.doc(summary=GET_DASHBOARD_STATS_SUMMARY, description=GET_DASHBOARD_STATS_DESCRIPTION)
def get_dashboard_stats():
    """
    Retrieve dashboard statistics.

    This endpoint returns consolidated counts for the dashboard including:
    - Total customers
    - Total employees
    - Total services
    - Appointment counts (total, past, upcoming)

    Responses:
        JSON response:
        - 200 (OK): Successfully retrieved dashboard statistics.
    """
    
    return {
        'customers': count_customers(),
        'employees': count_employees(),
        'services': get_services_count('available'),
        'appointments': {
            'total': get_appointments_count('all'),
            'past': get_appointments_count('past'),
            'upcoming': get_appointments_count('upcoming')
        }
    }

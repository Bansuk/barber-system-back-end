"""
Registers the customer-related routes with the Flask application.
"""

from flask_smorest import Api
from routes.customer_routes import customer_bp
from routes.employee_routes import employee_bp
from routes.service_routes import service_bp
from routes.appointment_routes import appointment_bp
from routes.dashboard_routes import dashboard_bp


def register_routes(api: Api):
    """
    Registers all application routes.

    Args:
        app (Flask): The Flask application instance.
    """

    api.register_blueprint(customer_bp)
    api.register_blueprint(employee_bp)
    api.register_blueprint(service_bp)
    api.register_blueprint(appointment_bp)
    api.register_blueprint(dashboard_bp)

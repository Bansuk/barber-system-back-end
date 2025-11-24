"""
Schema module for Service entities.
"""

from marshmallow import Schema, fields, validate

NAME_METADATA = metadata = {
    'example': 'Corte de Cabelo Masculino'}
NAME_DESCRIPTION = 'Nome do Serviço'
PRICE_METADATA = metadata = {
    'example': '4500'}
PRICE_DESCRIPTION = 'Preço do Serviço em centavos (4500 é equivalente $45,00)'


class ServiceSchema(Schema):
    """
    Schema for validating and serializing service input data.

    Attributes:
        name (str): The name of the service (min 3, max 100 characters).
        price (int): The service's price in cents.
    """

    name = fields.Str(required=True, metadata=NAME_METADATA,
                      descriptiom=NAME_DESCRIPTION, validate=validate.Length(min=3, max=100))
    price = fields.Int(
        required=True, metadata=PRICE_METADATA, description=PRICE_DESCRIPTION)


class ServiceViewSchema(Schema):
    """
    Schema for serializing employee data for output.

    Attributes:
        id (int): The unique identifier of the employee.
        name (str): The name of the employee.
        email (str): The employee's email address.
        employees (List[int]): The list of employees that can performe the service.
        appointment (List[int]): The list of appointment containing the service.
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, metadata=NAME_METADATA,
                      descriptiom=NAME_DESCRIPTION)
    price = fields.Int(
        required=True, metadata=PRICE_METADATA, description=PRICE_DESCRIPTION)
    employees = fields.List(
        fields.Pluck('EmployeeViewSchema', 'id'),
        required=True,
        metadata={'example': '[1]'},
        description='Lista dos funcionários que executam o serviço',
    )
    appointments = fields.List(
        fields.Pluck('AppointmentViewSchema', 'id'),
        required=True,
        metadata={'example': '[1]'},
        description='Lista dos agendamentos que possuem o serviço',
    )

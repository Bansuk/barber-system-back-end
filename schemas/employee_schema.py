"""
Schema module for Employee entities.
"""

from marshmallow import Schema, fields, validate

NAME_METADATA = {
    'example': 'Fulano de Tal'}
NAME_DESCRIPTION = 'Nome do Funcionário(a)'
EMAIL_METADATA = {
    'example': 'fulano@teste.com'}
EMAIL_DESCRIPTION = 'E-mail do Funcionário(a)'
PHONE_NUMBER_METADATA = {
    'example': '+5521999999999'}
PHONE_NUMBER_DESCRIPTION = 'Número celular do Funcionário(a)'
STATUS_METADATA = {
    'example': 'available'}
STATUS_DESCRIPTION = 'Status de disponibilidade do Funcionário(a) (available, vacation, sick_leave, unavailable)'
SERVICES_METADATA = {'example': '[1]'}
SERVICES_DESCRIPTION = 'Lista dos serviços executados pelo funcionário(a)'


class EmployeeSchema(Schema):
    """
    Schema for validating and deserializing employee input data.

    Attributes:
        name (str): The name of the employee (min 3, max 100 characters).
        email (str): The employee's email address.
        phone_number (str): The employee's cellphone number.
        service_ids (List[int]): The list of services performed by the employee.
    """

    name = fields.Str(required=True, metadata=NAME_METADATA,
                      description=NAME_DESCRIPTION, validate=validate.Length(min=3, max=100))
    email = fields.Email(
        required=True, metadata=EMAIL_METADATA, description=EMAIL_DESCRIPTION)
    phone_number = fields.Str(
        required=True, metadata=PHONE_NUMBER_METADATA, description=PHONE_NUMBER_DESCRIPTION)
    status = fields.Str(
        required=False,
        metadata=STATUS_METADATA,
        description=STATUS_DESCRIPTION,
        validate=validate.OneOf(['available', 'vacation', 'sick_leave', 'unavailable']),
        load_default='available'
    )
    service_ids = fields.List(
        fields.Int(),
        required=True,
        metadata=SERVICES_METADATA,
        description=SERVICES_DESCRIPTION,
        validate=validate.Length(min=1, max=10)
    )


class EmployeeViewSchema(Schema):
    """
    Schema for serializing employee data for output.

    Attributes:
        id (int): The unique identifier of the employee.
        name (str): The name of the employee.
        email (str): The employee's email address.
        phone_number (str): The employee's cellphone number.
        service_ids (List[int]): The list of services performed by the employee.
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, metadata=NAME_METADATA,
                      description=NAME_DESCRIPTION)
    email = fields.Email(
        required=True, metadata=EMAIL_METADATA, description=EMAIL_DESCRIPTION)
    phone_number = fields.Str(
        required=True, metadata=PHONE_NUMBER_METADATA, description=PHONE_NUMBER_DESCRIPTION)
    status = fields.Str(
        required=True,
        metadata=STATUS_METADATA,
        description=STATUS_DESCRIPTION
    )
    service_ids = fields.Method(
        'get_service_ids',
        metadata=SERVICES_METADATA,
        description=SERVICES_DESCRIPTION,
        dump_only=True
    )

    def get_service_ids(self, obj) -> list[int]:
        """
        Extract service IDs from the employee's related services.

        Attributes:
            obj (Employee): The employee instance whose service IDs
                should be retrieved.

        Returns:
            list[int]: A list of IDs corresponding to the services
                associated with the employee.
        """
        return [service.id for service in obj.services]

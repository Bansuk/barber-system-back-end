"""
Schema module for Customer entities.
"""

from marshmallow import Schema, fields, validate

NAME_METADATA = metadata = {
    'example': 'Fulano de Tal'}
NAME_DESCRIPTION = 'Nome do Cliente'
EMAIL_METADATA = {
    'example': 'fulano@teste.com'}
EMAIL_DESCRIPTION = 'E-mail do Cliente'
PHONE_NUMBER_METADATA = {
    'example': '+5521999999999'}
PHONE_NUMBER_DESCRIPTION = 'Número celular do cliente'


class CustomerSchema(Schema):
    """
    Schema for validating and serializing customer input data.

    Attributes:
        name (str): The name of the customer (min 3, max 100 characters).
        email (str): The customer's email address.
        phone_number (str): The customer's cellphone number.
    """

    name = fields.Str(required=True, metadata=NAME_METADATA,
                      description=NAME_DESCRIPTION, validate=validate.Length(min=3, max=100))
    email = fields.Email(
        required=True, metadata=EMAIL_METADATA, description=EMAIL_DESCRIPTION)
    phone_number = fields.Str(
        required=True, metadata=PHONE_NUMBER_METADATA, description=PHONE_NUMBER_DESCRIPTION)


class CustomerViewSchema(Schema):
    """
    Schema for serializing customer data for output.

    Attributes:
        id (int): The unique identifier of the customer.
        name (str): The name of the customer.
        email (str): The customer's email address.
        phone_number (str): The customer's cellphone number.
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, metadata=NAME_METADATA,
                      description=NAME_DESCRIPTION)
    email = fields.Email(
        required=True, metadata=EMAIL_METADATA, description=EMAIL_DESCRIPTION)
    phone_number = fields.Str(
        required=True, metadata=PHONE_NUMBER_METADATA, description=PHONE_NUMBER_DESCRIPTION)

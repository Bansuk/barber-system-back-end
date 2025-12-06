"""
This module contains standard descriptions and responses for the Customer API.
"""

from schemas.error_schema import ErrorSchema

DELETE_CUSTOMER_SUMMARY = 'Deleta as informações de um cliente.'
DELETE_CUSTOMER_DESCRIPTION = 'Este endpoint apaga as informações do cliente ' \
    'informado caso o mesmo seja encontrado.'
GET_CUSTOMER_SUMMARY = 'Retorna a lista de todos os clientes cadatrados.'
GET_CUSTOMER_DESCRIPTION = 'Este endpoint retorna uma coleção de cadastros de clientes ' \
    'no formato JSON.'
GET_CUSTOMER_COUNT_SUMMARY = 'Retorna o número total de clientes cadastrados.'
GET_CUSTOMER_COUNT_DESCRIPTION = 'Este endpoint retorna a contagem total de clientes ' \
    'registrados no sistema.'
POST_CUSTOMER_SUMMARY = 'Lida com a criação de um novo cliente.'
POST_CUSTOMER_DESCRIPTION = 'Este endpoint processa o envio de um formulário (JSON) ' \
    'para criar um novo registro de cliente.'
UPDATE_CUSTOMER_SUMMARY = 'Lida com a atualização de um cliente cadatrado.'
UPDATE_CUSTOMER_DESCRIPTION = 'Este endpoint processa o envio de um id e de um formulário (JSON) ' \
    'para atualizar um registro de cliente.'

delete_customer_responses = {
    400: {
        'description': 'Bad Request: O formato do id é inválido.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 400,
                    'errors': {
                        'json': ['Invalid customer id.']
                    },
                    'status': 'Bad Request'
                }
            }
        }
    },
    404: {
        'description': 'Not Found: O cliente informado não foi encontrado.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 404,
                    'errors': {
                        'json': ['Customer not found.']
                    },
                    'status': 'Not Found'
                }
            }
        }
    },
}
post_customer_responses = {
    400: {
        'description': 'Bad Request: O formato do corpo JSON é inválido.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 400,
                    'errors': {
                        'json': [
                            'Invalid JSON body.'
                        ]
                    },
                    'status': 'Bad Request'
                }
            }
        }
    },
    409: {
        'description': 'Conflict: O valor informado não está disponível.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 409,
                    'errors': {
                        'json': {
                            'email': ['Email already registered.'],
                            "phone_number": [
                                "Phone number already registered."
                            ]
                        }
                    },
                    'status': 'Conflict'
                }
            }
        }
    },
    422: {
        'description':
        'Validation Error: A requisição contém campos ausentes ou inválidos.\n\n'
        '**Motivos Possíveis:**\n'
        '- `name` é obrigatório, mas não foi fornecido.\n'
        '- `email` é obrigatório, mas não foi fornecido.\n'
        '- `email`: o formato do email é inválido (deve ser um endereço de e-mail válido).\n\n',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 422,
                    'errors': {
                        'json': {
                            'name': ['Missing data for required field.'],
                            'email': ['Missing data for required field.',
                                      'Not a valid email address.']
                        }
                    },
                    'status': 'Unprocessable Entity'
                }
            }
        }
    }
}
update_customer_responses = {
    400: {
        'description': 'Bad Request: O formato do corpo JSON é inválido.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 400,
                    'errors': {
                        'json': [
                            'Invalid JSON body.'
                        ]
                    },
                    'status': 'Bad Request'
                }
            }
        }
    },
    404: {
        'description': 'Not Found: O cliente informado não foi encontrado.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 404,
                    'errors': {
                        'json': ['Customer not found.']
                    },
                    'status': 'Not Found'
                }
            }
        }
    },
    409: {
        'description': 'Conflict: O valor informado não está disponivel.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 409,
                    'errors': {
                        'json': {
                            'email': ['Email already registered.'],
                            "phone_number": [
                                "Phone number already registered."
                            ]
                        }
                    },
                    'status': 'Conflict'
                }
            }
        }
    }
}

"""
This module contains standard descriptions and responses for the Employee API.
"""

from schemas.error_schema import ErrorSchema

DELETE_EMPLOYEE_SUMMARY = 'Deleta as informações de um funcionário(a).'
DELETE_EMPLOYEE_DESCRIPTION = 'Este endpoint apaga as informações do(a) funcionário(a) ' \
    'informado caso o(a) mesmo(a) seja encontrado(a).'
GET_EMPLOYEE_SUMMARY = 'Retorna a lista de todos os funcionários cadatrados.'
GET_EMPLOYEE_DESCRIPTION = 'Este endpoint retorna uma coleção de cadastros de funcionários ' \
    'no formato JSON.'
GET_EMPLOYEE_COUNT_SUMMARY = 'Retorna o número total de funcionários(as) cadastrados(as).'
GET_EMPLOYEE_COUNT_DESCRIPTION = 'Este endpoint retorna a contagem total de funcionários ' \
    'registrados no sistema.'
POST_EMPLOYEE_SUMMARY = 'Lida com a criação de um novo funcionário(a).'
POST_EMPLOYEE_DESCRIPTION = 'Este endpoint processa o envio de um formulário (JSON) ' \
    'para criar um novo registro de funcionário(a).'
UPDATE_EMPLOYEE_SUMMARY = 'Lida com a atualização de um funcionário(a) cadatrado(a).'
UPDATE_EMPLOYEE_DESCRIPTION = 'Este endpoint processa o envio de um id e de um formulário (JSON) ' \
    'para atualizar um registro de um(a) funcionário(a).'

post_employee_responses = {
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
        'description': 'Not Found: Algum(ns) dos serviços informados não foi(foram) encontrado(s).',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 404,
                    'errors': {
                        'json': {
                            'service': ['Service not found.']
                        }
                    },
                    'status': 'Not Found'
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
                            'name': ['Email already registered.'],
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
        '- `email`: o formato do email é inválido (deve ser um endereço de e-mail válido).\n'
        '- `service`: deve haver ao menos um serviço cadastrado antes de criar'
        'um funcionário(a).\n\n',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 422,
                    'errors': {
                        'json': {
                            'name': ['Missing data for required field.'],
                            'email': ['Missing data for required field.',
                                      'Not a valid email address.'],
                            'service': ['A service must be registered before'
                                        'registering an employee.']
                        }
                    },
                    'status': 'Unprocessable Entity'
                }
            }
        }
    }
}
delete_employee_responses = {
    400: {
        'description': 'Bad Request: O formato do id é inválido.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 400,
                    'errors': {
                        'json': ['Invalid employee id.']
                    },
                    'status': 'Bad Request'
                }
            }
        }
    },
    404: {
        'description': 'Not Found: O funcionário(a) informado não foi encontrado.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 404,
                    'errors': {
                        'json': ['Employee not found.']
                    },
                    'status': 'Not Found'
                }
            }
        }
    },
}
update_employee_responses = {
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
        'description': 'Not Found: O funcionário(a) informado não foi encontrado.',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 404,
                    'errors': {
                        'json': ['Employee not found.']
                    },
                    'status': 'Not Found'
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
        'Validation Error: O formato do eamil fornecido é inválido.\n\n',
        'content': {
            'application/json': {
                'schema': ErrorSchema,
                'example': {
                    'code': 422,
                    'errors': {
                        'json': {
                            'email': ['Not a valid email address.'],
                        }
                    },
                    'status': 'Unprocessable Entity'
                }
            }
        }
    }
}

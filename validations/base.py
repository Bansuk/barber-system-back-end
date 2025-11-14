"""
Validation module for all entities.
"""

from flask_smorest import abort


class BaseValidation:
    @staticmethod
    def _abort_bad_request(message: str, field: str = 'json') -> None:
        abort(400, errors={field: [message]})

    @staticmethod
    def validate_positive_int(value: any, name: str = 'id') -> None:
        if not isinstance(value, int) or value <= 0:
            BaseValidation._abort_bad_request(f'Invalid {name}.')

"""
Business module for all entities.
"""

from flask_smorest import abort
from validations.base import BaseValidation


class BaseBusiness:
    """
    Base business class providing common business utilities.
    """


def get_or_404(getter, entity_id: int, name: str):
    """
    Fetch an entity or abort with 404.

    Args:
        getter: Function used to search for the entity.
        entity_id: ID of the entity searched.
        name: Name of the entity.

    Returns:
        object: Found entity.

    Raises:
        HTTPException: Raises a 404 (Not Found) if entity was not found.
    """
    BaseValidation.validate_positive_int(entity_id, name)
    entity = getter(entity_id)
    if entity is None:
        abort(404, errors={
              'json': {name: [f'{name.capitalize()} not found.']}})
    return entity

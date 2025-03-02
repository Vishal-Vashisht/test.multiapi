from typing import NamedTuple
from ..entity.entity import Entity


class APIConfig(NamedTuple):

    id: int = 0
    name: str = ""
    route: str = ""
    method: str = ""
    description: str = ""
    body: dict = {}
    query_params: dict = {}
    response: list = ["*"]
    is_authenticated: bool = True
    entity: Entity = Entity

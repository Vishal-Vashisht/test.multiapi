from typing import NamedTuple


class Entity(NamedTuple):

    pk: int = 0
    entity_name: str = ""
    entity_alias: str = ""
    columns_config: str = ""
    relations_config: str = ""

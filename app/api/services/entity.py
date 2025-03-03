import ast

from jsonschema import Draft7Validator
from sqlalchemy import text

from app.api.models.models import Entity, db
from app.constants import DATA_TYPE_MAPPING, DEFAULT_COLUMN, logger
from app.utils import ValidationError, realtion_schema, schema_columns, serialize_response


def perform_validation(entity):
    if not entity.entity_alias:
        raise ValidationError({"error": "entity alias is required"})
    if not entity.entity_name:
        raise ValidationError({"error": "entity name is required"})

    if not entity.columns_config:
        raise ValidationError({"error": "column config is reuired"})

    if not (
        isinstance(entity.columns_config, dict)
        or isinstance(entity.relations_config, dict)
    ):
        raise ValidationError({"error": "Config is not valid"})

    if Entity.query.filter_by(entity_name=entity.entity_name).first():
        raise ValidationError({"error": "Entity already exists"})


def schema_validation(entity):

    validate_columns_and_relation_config(entity)


def validate_columns_and_relation_config(entity):

    validator_columns = Draft7Validator(schema_columns)
    errors = []
    for e in validator_columns.iter_errors(entity.columns_config):
        errors.append({"name": e.path[0], "error": e.message})

    validator_relations = Draft7Validator(realtion_schema)
    for e in validator_relations.iter_errors(entity.relations_config):
        errors.append({"name": e.path[0], "error": e.message})
    if errors:
        raise ValidationError(errors)


def create_entity(entity):
    CREAT_SCRIPT = f"CREATE TABLE IF NOT EXISTS {entity.entity_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, "
    col_config = entity.columns_config
    col_relation = entity.relations_config
    columns = ""

    REL_STR = ""
    if col_relation:

        for ind, (rel_name, rel_val) in enumerate(col_relation.items(), 1):

            rel_raw_entity = rel_val.get("entity")
            raw_rel_column = rel_val.get("column")
            raw_ref_column = rel_val.get("ref_column")
            rel_entity = Entity.query.get(rel_raw_entity)
            if not rel_entity:
                raise ValidationError(
                    {
                        "error": "Table not exist, remove this relation for proceeding further."
                    }
                )

            if raw_rel_column not in col_config and raw_rel_column.lower() != "id":
                raise ValidationError({"error": "Column not found in column config."})

            table_columns = ast.literal_eval(rel_entity.columns_config)
            rel_column = table_columns.get(raw_ref_column)
            if not rel_column:
                raise ValidationError(
                    {
                        "error": "Column not exist, in refrence table remove this relation for proceeding further."
                    }
                )

            REL_STR += f""",CONSTRAINT {rel_name} FOREIGN KEY ({raw_rel_column}) REFERENCES
            {rel_entity.entity_name}({raw_ref_column})"""

    for ind, (col_name, col_val) in enumerate(col_config.items(), 1):

        d_type = DATA_TYPE_MAPPING.get(col_val.get("type", "VARCHAR"))
        length = col_val.get("length", "")
        constraint = col_val.get("constraint", "")
        if ind == len(col_config):
            columns += f"""{col_name} {d_type}"""
        else:
            columns += f"""{col_name} {d_type}"""
        if length:
            columns += f"({str(length)})"

        if ind == len(col_config):
            columns += f" {constraint}"
        else:
            columns += f" {constraint},"

    CREAT_SCRIPT += f"{columns}{REL_STR})"
    logger.info("Script %s", CREAT_SCRIPT)
    db.session.execute(text(CREAT_SCRIPT))

    col_config.update(DEFAULT_COLUMN)
    entity_instance = Entity(
        entity_name=entity.entity_name,
        entity_alias=entity.entity_alias,
        columns_config=str(entity.columns_config),
        relations_config=str(entity.relations_config),
    )
    entity_instance.save()

    return {
        "entity": entity_instance.entity_name,
        "pk": entity_instance.id,
        "alias": entity_instance.entity_alias,
    }


def get_data(request, pk):

    query_params = request.query_params
    query_set = Entity.query.all()
    page = query_params.pop("page", 1)
    page_size = query_params.pop("page_size", 10)
    if pk:
        query_set = Entity.query.get(pk)
    if query_params:
        query_set = Entity.query.filter_by(**query_params).all()

    resp = serialize_response(query_set, ["*"], Entity)
    return resp
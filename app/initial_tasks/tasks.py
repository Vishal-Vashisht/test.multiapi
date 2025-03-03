import ast
import re
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    LargeBinary,
    String,
    inspect,
)

from app.api.models.models import APIConfig, DB_Datatypes, Entity, db
from app.utils import customize_route


def task(app, dynamic_bp):
    with app.app_context():
        register_datatypes_in_app(app)
        update_custom_config(app, dynamic_bp)
        register_models(app)


def register_models(app):

    if not validate_table_in_db(Entity.__tablename__):
        return
    entities = Entity.query.all()

    for entity in entities:
        if hasattr(app, "dynamic_models"):
            if entity.entity_name in app.dynamic_models:
                return
        # Create SQLAlchemy model class dynamically
        columns = ast.literal_eval(entity.columns_config)
        attrs = {
            "__tablename__": entity.entity_name,
            "id": Column(Integer, primary_key=True),
        }

        d_types = app.db_datatypes
        d_types_without_length = app.dtypes_without_length
        # Add columns based on definition
        for col_name, col_val in columns.items():
            if col_name == "id":  # Skip id as it's already defined
                continue

            allow_length = True
            data_type = col_val.get("type", "int")
            if data_type in d_types_without_length:
                allow_length = False
            d_data_type = d_data_type = getattr(Column, d_types.get(data_type, "String"), String)
            if allow_length:
                length = col_val.get("length", 255)
                attrs[col_name] = Column(d_data_type(length))
            else:
                attrs[col_name] = Column(d_data_type)
            # Add more data types as needed

        # Create and register the model class
        model_class = type(entity.entity_name.capitalize(), (db.Model,), attrs)

        def serialize(self):
            """Serialize the model instance into a dictionary."""
            data = {}
            # Loop through all columns defined in the model
            for column in self.__table__.columns:
                data[column.name] = getattr(self, column.name)
            return data

        model_class.serialize = serialize
        # Store in a global registry for later use
        if not hasattr(app, "dynamic_models"):
            app.dynamic_models = {}
        app.dynamic_models[entity.entity_name] = model_class


def update_custom_config(app, dynamic_bp):

    api_config = app.config.get("API_CONFIG", {})
    # Logic to remove URLS what didn't work
    # print("app.url_map", app.url_map.__dict__)
    # for view_name in list(app.view_functions.keys()):
    #     if "dynamic_apis" in view_name:
    #         del app.view_functions[view_name]
    # remove_url_rules(app, dynamic_bp)
    if not validate_table_in_db(APIConfig.__tablename__):
        return
    api_config_data = APIConfig.query.all()
    if app.blueprints.get("dynamic_apis"):
        del app.blueprints["dynamic_apis"]
    for api_data in api_config_data:
        add_route_to_api_config(api_data, api_config)
        register_routes_in_blueprint(api_data, dynamic_bp)

    app.register_blueprint(dynamic_bp)


def validate_table_in_db(table_name):
    inspector = inspect(db.engine)
    return inspector.has_table(table_name)


def add_route_to_api_config(api_data, api_config):
    if api_data.route in api_config:
        return
    api_route = customize_route(api_data.route)
    group = api_data.entity_rel.entity_alias

    api_config.update(
        {
            f"/api/v1/{api_route}": {
                "methods": set((api_data.method.upper(),)),
                "is_authenticated": api_data.is_authenticated,
                f"{api_data.method.upper()}_data": {
                    "body": ast.literal_eval(api_data.body),
                    "query_params": ast.literal_eval(api_data.query_params),
                    "summary": api_data.description,
                },
                "group": group,
            }
        }
    )


def register_routes_in_blueprint(api_data, dynamic_bp):
    api_route = customize_route(api_data.route)
    seen = set(())
    if api_route in seen:
        return
    seen.add(api_route)
    dynamic_bp.add_url_rule(
        api_route,
        view_func=dynamic_bp.view_class.as_view(f"{api_data.method}{uuid.uuid1()}"),
    )


def remove_url_rules(app, bp):
    endpoint_prefix = "dynamic_apis."
    # Clean up URL map
    rules_to_remove = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint.startswith(endpoint_prefix):
            rules_to_remove.append(rule)

    for rule in rules_to_remove:
        app.url_map._rules.remove(rule)
        if rule.endpoint in app.url_map._rules_by_endpoint:
            del app.url_map._rules_by_endpoint[rule.endpoint]

    # Create and register fresh blueprint
    new_bp = bp
    app.register_blueprint(new_bp)


def register_datatypes_in_app(app):

    if not validate_table_in_db(DB_Datatypes.__tablename__):
        return
    data = DB_Datatypes.query.all()
    datatypes = {}
    for dtype_ins in data:
        datatypes[dtype_ins.data_type] = dtype_ins.s_data_type
    app.db_datatypes = datatypes
    app.dtypes_without_length = {
        "INTEGER",
        "REAL",
        "BLOB",
        "BOOLEAN",
        "DATE",
        "DATETIME",
        "TIMESTAMP",
    }

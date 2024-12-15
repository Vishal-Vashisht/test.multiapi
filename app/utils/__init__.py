from app.api.models.models import db
from sqlalchemy import inspect, text
from app.constants import logger

MAIN_DB = set(("postgresql", "mysql", "oracle"))
NOT_DELETE_TABLE = set((
    "alembic_version", "daily_data_delete",
    "internal_users", "task_status",
    "bg_task_response", "bg_tasks"))


def paginate_response(page, page_size, query):

    offset = (page-1) * page_size
    return query.offset(offset).limit(page_size).all(), query.count()


def delete_sqllite_data():

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    for table in tables:
        if table in NOT_DELETE_TABLE:
            continue
        db.session.execute(text(f'DELETE FROM {table};'))
        logger.info("deleted data for %s", table)

    db.session.commit()
    db.session.execute(text('VACUUM;'))
    db.session.commit()
    logger.info("Database compacted and all rows deleted.")


def delete_main_db_data(dialect):

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    for table in tables:
        if table in NOT_DELETE_TABLE:
            continue
        if dialect == "postgresql":
            db.session.execute(text(f'TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;'))
        else:
            db.session.execute(text(f'TRUNCATE TABLE {table};'))
    db.session.commit()
    logger.info("Database compacted and all rows deleted.")

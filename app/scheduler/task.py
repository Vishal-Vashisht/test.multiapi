from app.api.models.models import db, DailyDataDelete
import datetime
from sqlalchemy import inspect, text

MAIN_DB = set(("postgresql", "mysql", "oracle"))
NOT_DELETE_TABLE = set(("alembic_version", "daily_data_delete"))


def Delete_database_data(app):
    with app.app_context():
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(23, 55, 0)  # 23:55:00
        end_time = datetime.time(0, 10, 0)     # 00:10:00

        current_date = datetime.datetime.now().date()
        event_date_in_db = DailyDataDelete.query.filter(
            DailyDataDelete.event_date == current_date).first()

        if ((start_time <= current_time or current_time <= end_time) and not event_date_in_db):
            print("current time: ->", current_time,
                  "start_time: -> ", start_time,
                  "end time: -> ", end_time)
            try:
                print("Performing data cleanup task", event_date_in_db)

                dialect = db.engine.dialect.name.lower()
                if dialect == "sqlite":
                    delete_sqllite_data()
                elif dialect in MAIN_DB:
                    delete_main_db_data()

                # Insert a new event date entry to prevent running again
                insert_event_date = DailyDataDelete(
                    process_name="Data Cleanup",
                    event_date=current_date
                )

                # Save to the database
                insert_event_date.save()
            except Exception as e:
                print("Error in data cleanup ->", str(e))


def delete_sqllite_data():

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    for table in tables:
        if table in NOT_DELETE_TABLE:
            continue
        db.session.execute(text(f'DELETE FROM {table};'))
        print("deleted data for", table)

    db.session.commit()
    db.session.execute(text('VACUUM;'))
    db.session.commit()
    print("Database compacted and all rows deleted.")


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
    print("Database compacted and all rows deleted.")
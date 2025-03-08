import datetime

from app.api.models.models import DailyDataDelete, db
from app.utils import (
    delete_main_db_data,
    delete_sqllite_data,
    )
from app.constants import logger, MAIN_DB


def Delete_database_data(app):
    with app.app_context():
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(23, 55, 0)  # 23:55:00
        end_time = datetime.time(0, 10, 0)     # 00:10:00

        current_date = datetime.datetime.now().date()
        event_date_in_db = DailyDataDelete.query.filter(
            DailyDataDelete.event_date == current_date).first()

        if ((start_time <= current_time or current_time <= end_time) and not event_date_in_db):
            logger.info("current time: -> %s", current_time)
            logger.info("start_time: -> %s", start_time)
            logger.info("end time: -> %s", end_time)

            try:
                logger.info(
                    "Performing data cleanup task %s", event_date_in_db)

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
                logger.info("Error in data cleanup ->%s", str(e))

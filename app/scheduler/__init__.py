from apscheduler.schedulers.background import BackgroundScheduler
from .task import Delete_database_data


def register_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(Delete_database_data, "interval", seconds=5, args=[app])
    scheduler.start()

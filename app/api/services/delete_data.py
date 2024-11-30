import json
from app.utils import (
    delete_main_db_data,
    delete_sqllite_data,
    MAIN_DB)

from app.api.models.models import db, BGTasks, TaskStatus, BGTaskResponse
from app.constants import logger


def delete_data_async(app, thread_id):

    with app.app_context():  # Push the app context to the background thread
        (task_status_start,
         task_status_finish,
         task_status_error) = get_statuses()

        bgtask_inst = BGTasks(
            task_name="Delete db data",
            task_status=task_status_start.status_id,
            task_id=thread_id
        )
        bgtask_inst.save()
        dialect = db.engine.dialect.name.lower()
        try:
            if dialect == "sqlite":
                delete_sqllite_data()
            elif dialect in MAIN_DB:
                delete_main_db_data()
            bgtask_inst.task_status = task_status_finish.status_id
            response = {"msg": "success"}
        except Exception as e:
            logger.info(str(e))
            bgtask_inst.task_status = task_status_error.status_id
            response["error"] = str(e)
            response["msg"] = "error"
        finally:
            db.session.commit()
            task_resp = BGTaskResponse(
                response=json.dumps(response),
                task_id=bgtask_inst.id
            )
            task_resp.save()


def delete_data_sync(app, thread_id):

    (task_status_start,
     task_status_finish,
     task_status_error) = get_statuses()

    bgtask_inst = BGTasks(
        task_name="Delete db data",
        task_status=task_status_start.status_id,
        task_id=thread_id
    )
    bgtask_inst.save()
    dialect = db.engine.dialect.name.lower()
    try:
        if dialect == "sqlite":
            delete_sqllite_data()
        elif dialect in MAIN_DB:
            delete_main_db_data()
        bgtask_inst.task_status = task_status_finish.status_id
        response = {"msg": "success"}
    except Exception as e:
        logger.info(str(e))
        bgtask_inst.task_status = task_status_error.status_id
        response["error"] = str(e)
        response["msg"] = "error"
    finally:
        db.session.commit()
        task_resp = BGTaskResponse(
            response=json.dumps(response),
            task_id=bgtask_inst.id
        )
        task_resp.save()

        return {
            "status": bgtask_inst.task_status_ref.status_name,
            "response": task_resp.response,
            "process_id": bgtask_inst.task_id
        }


def get_statuses():

    task_status_start = TaskStatus.get_status("in-progress")
    task_status_finish = TaskStatus.get_status("complete")
    task_status_error = TaskStatus.get_status("error")

    return task_status_start, task_status_finish, task_status_error

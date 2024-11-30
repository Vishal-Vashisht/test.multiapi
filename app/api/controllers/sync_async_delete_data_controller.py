import uuid
from threading import Thread

from flask import Blueprint, current_app, request
from flask.views import MethodView

from app.api.services.delete_data import delete_data
from app.api.models.models import BGTasks, BGTaskResponse


class ListDeleteDataAPIView(MethodView):

    def post(self):

        try:
            app = current_app._get_current_object()
            thread_id = uuid.uuid4()
            t1 = Thread(target=delete_data, args=(app, str(thread_id)))
            t1.start()
            return {"msg": "success", "process_id": thread_id}
        except Exception as e:
            return {"msg": "Inernal server error", "error": str(e)}

    def get(self):

        process_id = request.args.get("process_id")
        if not process_id:
            return {
                "msg": "error",
                "errors": ["process_id is required"]
            }, 400

        process = BGTasks.get_task(process_id)
        if not process:
            return {
                "msg": "error",
                "errors": ["No process found"]
            }, 400

        response = BGTaskResponse.query.filter_by(task_id=process.id).first()

        return {
            "status": process.task_status_ref.status_name,
            "response": response.response
        }


class SyncDeletAPIView(MethodView):

    def post(self):

        try:
            app = current_app._get_current_object()
            thread_id = uuid.uuid4()
            delete_data(app, str(thread_id))
            return {"msg": "success", "process_id": thread_id}
        except Exception as e:
            return {"msg": "Inernal server error", "error": str(e)}

delete_data_bp = Blueprint("delete_data_type", __name__, url_prefix="/api/v1/tables/") # noqa
delete_data_bp.add_url_rule("async/delete/", view_func=ListDeleteDataAPIView.as_view("delete_data"), methods=["POST"]) # noqa
delete_data_bp.add_url_rule("task/info/", view_func=ListDeleteDataAPIView.as_view("get_data"), methods=["GET"]) # noqa
delete_data_bp.add_url_rule("sync/delete/", view_func=ListDeleteDataAPIView.as_view("SyncDeletAPIView")) # noqa
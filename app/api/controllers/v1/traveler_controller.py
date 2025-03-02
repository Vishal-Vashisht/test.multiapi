from flask import Blueprint, request, jsonify
from flask.views import MethodView
import json


class TravlerList(MethodView):

    def get(self):

        data = [{
            "stay_time": "00-06-00",
            "location": "{'address': 'Sunshine Coast QLD, Australia', 'location': {'coordinates': [-26.65, 153.066667]}}",
            "end_address": "{}",
            "product_type": "Attraction",
            "attraction_type": "['Tours']",
            "have_different_address": False,
            "opening_hours": "[\n  {\n    \"modified_at\": \"May 28 2024, 08:16:19\",\n    \"is_deleted\": False,\n    \"is_active\": true,\n    \"extra_data\": {},\n    \"end_month\": \"December\",\n    \"start_month\": \"January\",\n    \"friday_end_time\": \"\",\n    \"monday_end_time\": \"\",\n    \"sunday_end_time\": \"\",\n    \"tuesday_end_time\": \"\",\n    \"friday_start_time\": \"\",\n    \"monday_start_time\": \"\",\n    \"saturday_end_time\": \"\",\n    \"sunday_start_time\": \"\",\n    \"tuesday_start_time\": \"\",\n    \"wednesday_end_time\": \"15:00:00\",\n    \"saturday_start_time\": \"\",\n    \"wednesday_start_time\": \"09:00:00\",\n    \"pk\": 3944,\n    \"thursday_end_time\": \"\",\n    \"thursday_start_time\": \"\"\n  }\n]",
            "id": 3898,
            "name": "Eumundi Markets Guided Tour with Lunch"
        }]

        return json.dumps(data), 200


travler_bp = Blueprint("travler", __name__, url_prefix="/api/v1/trvlr")
travler_bp.add_url_rule("/", view_func=TravlerList.as_view("TravlerList")) # noqa

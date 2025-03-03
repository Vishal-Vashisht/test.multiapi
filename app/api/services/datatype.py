from app.api.models.models import DB_Datatypes, db
from app.utils import (
    serialize_response,
)


def get_data(request, pk):

    query_params = request.query_params
    query_set = DB_Datatypes.query.all()
    page = query_params.pop("page", 1)
    page_size = query_params.pop("page_size", 10)
    if pk:
        query_set = DB_Datatypes.query.get(pk)
    if query_params:
        query_set = DB_Datatypes.query.filter_by(**query_params).all()

    resp = serialize_response(query_set, ["*"], DB_Datatypes)
    return resp

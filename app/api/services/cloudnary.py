import io
import json
from flask import request
import cloudinary.uploader
from app.api.models.models import FileServices, FilesDetails
from app import constants


def cloudnary_upload():

    response = []
    for file in request.files.values():
        in_memory = io.BytesIO(file.read())
        in_memory.seek(0)
        upload_result = cloudinary.uploader.upload(
            in_memory,
            public_id=file.filename,
            resource_type="raw",
            **{"content_type": str(file.mimetype)}
        )

        file_service = FileServices.query.filter_by(
            servicename=constants.FILE_SERVICE_CLOUDNARY
        ).first()

        upload_result.pop("api_key", None)

        FilesDetails(
            filename=upload_result.get("display_name"),
            file_id=upload_result.get("asset_id"),
            extra_data=json.dumps(upload_result),
            link=upload_result.get("secure_url"),
            fileservice=file_service.id,
        ).save()
        response.append(
            {
                "secure_url": upload_result.get("secure_url"),
                "file_name": file.filename
            }
        )

    return {"response": "success", "results": response}, 201

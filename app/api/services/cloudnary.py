import io
from flask import request
import cloudinary.uploader


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
        response.append(
            {
                "secure_url": upload_result.get("secure_url"),
                "file_name": file.filename
            }
        )

    return {"response": "success", "results": response}, 201

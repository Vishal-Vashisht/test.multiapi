import cloudinary


def init_cloudnary_client(app):

    cloundnary_config_ins = cloudinary.config(
        cloud_name=app.config.get("CLOUDNARY_NAME"),
        api_key=app.config.get("CLOUDNARY_API_KEY"),
        api_secret=app.config.get("CLOUDNARY_API_SECRET"),  # Click 'View API Keys' above to copy your API secret
        secure=True,
    )

    app.cloudnary_ins = cloundnary_config_ins

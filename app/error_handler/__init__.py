from flask import Flask, render_template, request, abort
import werkzeug


def initialize_error_handler(app):
    register_error_handler(app)


def register_error_handler(app):

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("error.html"), 404

    @app.errorhandler(werkzeug.exceptions.HTTPException)
    def internal_error(error):
        return render_template("error.html"), 500

    @app.errorhandler(503)
    def not_found_error(error):
        return render_template("error.html"), 503

"""
The __init__.py serves double duty:
    * it will contain the application factory, and
    * it tells Python that the the directory should be treated as a package.
"""

from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)  # creates the Flask instance
    app.config.from_mapping(
        SECRET_KEY='dev',  # should be overridden with a random value when deploying
    )

    # Import and register the blueprints
    from . import dashboard
    app.register_blueprint(dashboard.bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

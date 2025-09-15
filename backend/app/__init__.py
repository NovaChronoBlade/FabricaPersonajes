from flask import Flask


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    # Simple config; extend as needed
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    # Register blueprints / routes
    from .routes import bp

    app.register_blueprint(bp)

    return app

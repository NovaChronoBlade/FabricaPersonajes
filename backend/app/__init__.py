import os
from flask import send_from_directory
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    # Simple config; extend as needed
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    # Register blueprints / routes
    from .routes import bp

    # Intentar ubicar la carpeta `public` en la raiz del proyecto. Originalmente
    # se construía relativo a `backend/`, lo cual provoca 404 si la carpeta
    # `public/` está al nivel superior del repo (como en esta estructura).
    # Subir hasta 5 niveles buscando `shared-config.json` o `public`.
    candidate = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for _ in range(6):
        if os.path.exists(os.path.join(candidate, 'shared-config.json')) or os.path.isdir(os.path.join(candidate, 'public')):
            break
        parent = os.path.dirname(candidate)
        if parent == candidate:
            break
        candidate = parent

    PUBLIC_DIR = os.path.join(candidate, 'public')

    @app.route('/images/<path:filename>')
    def serve_images(filename):
        # Servir desde PUBLIC_DIR/images; use send_from_directory que manejará seguridad
        images_dir = os.path.join(PUBLIC_DIR, 'images')
        return send_from_directory(images_dir, filename)


    app.register_blueprint(bp)

    CORS(app)  # Habilitar CORS para todas las rutas



    return app

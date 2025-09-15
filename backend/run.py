"""Launcher for the Flask backend package.

Run with: python -m backend.run
"""

try:
    from backend.app import create_app
except Exception:
    # Al ejecutar `python backend/run.py` es posible que el paquete no esté
    # en sys.path; añadir el directorio padre para permitir importaciones
    import os
    import sys

    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if pkg_root not in sys.path:
        sys.path.insert(0, pkg_root)

    from backend.app import create_app


def main():
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()

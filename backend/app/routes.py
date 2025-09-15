from flask import Blueprint, send_from_directory, request, Response
import json
from typing import Dict, Type
import os
from pathlib import Path

from .factories import FabricarElfos, FabricarEnanos, FabricarHumanos, FabricarOrcos
from .utils.image_manager import image_manager

bp = Blueprint("api", __name__, url_prefix="/api")


FACTORIES = {
    "elfos": FabricarElfos,
    "enanos": FabricarEnanos,
    "humanos": FabricarHumanos,
    "orcos": FabricarOrcos,
}


@bp.route("/factories", methods=["GET"])
def list_factories():
    return make_json_response(list(FACTORIES.keys()))


@bp.route("/create/<kind>", methods=["GET"])
def create_sample(kind: str):
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)

    fabrica = Factory()
    cuerpo = fabrica.crear_cuerpo()
    montura = fabrica.crear_montura()
    armadura = fabrica.crear_armadura()
    arma = fabrica.crear_arma()

    # Ejecutar métodos de acción
    cuerpo.analizar()
    montura.montar()
    armadura.equipar()
    arma.atacar()

    # Obtener información con imágenes
    personaje_info = {
        "status": "created",
        "kind": kind,
        "character": {
            "cuerpo": cuerpo.obtener_informacion(),
            "montura": montura.obtener_informacion(),
            "armadura": armadura.obtener_informacion(),
            "arma": arma.obtener_informacion()
        }
    }

    return make_json_response(personaje_info)


@bp.route("/images/<category>", methods=["GET"])
def list_images(category: str):
    """Lista todas las imágenes de una categoría"""
    if category not in ['characters', 'avatars', 'ui']:
        return make_json_response({"error": "Invalid category"}, status=400)
    
    images = image_manager.list_images(category)
    return make_json_response({
        "category": category,
        "images": [image_manager.get_web_path(category, img) for img in images]
    })


@bp.route("/images/<category>/<filename>", methods=["GET"])
def serve_image(category: str, filename: str):
    """Sirve una imagen específica"""
    if category not in ['characters', 'avatars', 'ui']:
        return make_json_response({"error": "Invalid category"}, status=400)
    
    try:
        image_path = image_manager.get_image_path(category)
        return send_from_directory(str(image_path), filename)
    except FileNotFoundError:
        return make_json_response({"error": "Image not found"}, status=404)


@bp.route("/upload/<category>", methods=["POST"])
def upload_image(category: str):
    """Sube una imagen a una categoría específica"""
    if category not in ['characters', 'avatars', 'ui']:
        return make_json_response({"error": "Invalid category"}, status=400)
    
    if 'image' not in request.files:
        return make_json_response({"error": "No image file provided"}, status=400)
    
    file = request.files['image']
    if file.filename == '':
        return make_json_response({"error": "No file selected"}, status=400)
    
    # Validar extensión del archivo
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        return make_json_response({"error": "Invalid file type"}, status=400)
    
    try:
        web_path = image_manager.save_image(category, file.filename, file.read())
        return make_json_response({
            "message": "Image uploaded successfully",
            "path": web_path
        })
    except Exception as e:
        return make_json_response({"error": str(e)}, status=500)


@bp.route("/character/<kind>/info", methods=["GET"])
def get_character_info(kind: str):
    """Obtiene información detallada de un personaje sin crear instancia"""
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "unknown factory"}, status=404)

    fabrica = Factory()
    cuerpo = fabrica.crear_cuerpo()
    montura = fabrica.crear_montura()
    armadura = fabrica.crear_armadura()
    arma = fabrica.crear_arma()

    character_info = {
        "kind": kind,
        "cuerpo": cuerpo.obtener_informacion(),
        "montura": montura.obtener_informacion(),
        "armadura": armadura.obtener_informacion(),
        "arma": arma.obtener_informacion()
    }

    return make_json_response(character_info)


def make_json_response(obj, status=200):
    """Serialize to JSON preserving unicode and ordering, set charset utf-8."""
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=False)
    return Response(payload, status=status, mimetype='application/json; charset=utf-8')

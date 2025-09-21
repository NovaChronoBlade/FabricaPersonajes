from flask import Blueprint, send_from_directory, request, Response
import json
import time
from typing import Dict, Type
import os
from pathlib import Path

from .factories import FabricarElfos, FabricarEnanos, FabricarHumanos, FabricarOrcos
from .patterns.singleton_pool import Pool
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


@bp.route("/pool/status", methods=["GET"])
def get_pool_status():
    """Obtiene el estado actual del pool singleton"""
    pool = Pool()
    return make_json_response(pool.get_current_factory_info())


@bp.route("/pool/delete/<kind>", methods=["DELETE", "POST"])
def delete_factory_from_pool(kind: str):
    """
    Elimina una fábrica específica del pool singleton.
    Solo permite eliminar si es la misma fábrica que está actualmente en uso.
    """
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    pool = Pool()
    current_info = pool.get_current_factory_info()
    
    # Intentar eliminar la fábrica específica
    success = pool.remove_factory(Factory)
    
    if success:
        return make_json_response({
            "message": f"Fabrica '{kind}' eliminada del pool exitosamente",
            "deleted_factory": kind,
            "previous_factory": current_info,
            "success": True
        })
    else:
        return make_json_response({
            "error": "No se puede eliminar la fábrica",
            "message": f"La fábrica actual en el pool es '{current_info['factory_type']}', no se puede eliminar '{kind}'",
            "current_factory": current_info,
            "requested_deletion": kind,
            "success": False
        }, status=400)


@bp.route("/pool/force-clear", methods=["DELETE", "POST"])
def force_clear_pool():
    """
    Fuerza la eliminación de cualquier fábrica del pool (sin validación de tipo).
    Usar con cuidado - elimina cualquier fábrica sin importar el tipo.
    """
    pool = Pool()
    current_info = pool.get_current_factory_info()
    
    # Forzar eliminación sin validación
    pool.remove_factory()  # Sin parámetros = eliminar cualquier fábrica
    
    return make_json_response({
        "message": "Pool limpiado forzadamente",
        "previous_factory": current_info,
        "success": True,
        "warning": "Se eliminó cualquier fábrica sin validación de tipo"
    })


@bp.route("/create/<kind>", methods=["GET", "POST"])
def create_sample(kind: str):
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    try:

        # Manejar parámetro delete
        delete_param = request.args.get('delete', '').lower()
        if delete_param == 'true':
            pool = Pool()
            current_info = pool.get_current_factory_info()
            
            # Intentar eliminar la fábrica específica
            success = pool.remove_factory(Factory)
            
            if success:
                return make_json_response({
                    "message": f"Fabrica '{kind}' eliminada del pool exitosamente",
                    "deleted_factory": kind,
                    "previous_factory": current_info
                })
            else:
                return make_json_response({
                    "error": "No se puede eliminar la fábrica",
                    "message": f"La fábrica actual en el pool es '{current_info['factory_type']}', no se puede eliminar '{kind}'",
                    "current_factory": current_info,
                    "requested_deletion": kind
                }, status=400)

        pool = Pool()

        fabrica = pool.get_factory(Factory)
        


        # Obtener objetos del pool con timeout personalizable
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
            },
        }


        return make_json_response(personaje_info)
        
    except RuntimeError as e:
        stats = fabrica.get_pool_stats() if 'fabrica' in locals() else {}
        return make_json_response({
            "error": "Pool exhausted",
            "message": str(e),
            "kind": kind,
            "pool_stats": stats,
            "suggestion": f"Usar /pools/{kind}/clear o esperar a que se devuelvan objetos"
        }, status=429)  # Too Many Requests
    except Exception as e:
        return make_json_response({
            "error": "Internal error", 
            "message": str(e),
            "kind": kind
        }, status=500)


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
    """Obtiene información detallada de un personaje usando el pool singleton"""
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "unknown factory"}, status=404)

    # Usar Singleton - siempre obtenemos la misma instancia
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
        "arma": arma.obtener_informacion(),
        "pool_stats": fabrica.get_pool_stats()
    }

    # Devolver objetos al pool para reutilización
    fabrica.devolver_cuerpo(cuerpo)
    fabrica.devolver_montura(montura) 
    fabrica.devolver_armadura(armadura)
    fabrica.devolver_arma(arma)

    return make_json_response(character_info)

def make_json_response(obj, status=200):
    """Serialize to JSON preserving unicode and ordering, set charset utf-8."""
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=False)
    return Response(payload, status=status, mimetype='application/json; charset=utf-8')

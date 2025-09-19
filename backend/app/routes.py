from flask import Blueprint, send_from_directory, request, Response
import json
import time
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


@bp.route("/create/<kind>", methods=["GET", "POST"])
def create_sample(kind: str):
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)

    # Obtener parámetros opcionales
    auto_return = request.args.get('auto_return', 'true').lower() == 'true'
    timeout = int(request.args.get('timeout', 10))
    
    try:
        # Usar Singleton - siempre obtenemos la misma instancia
        fabrica = Factory()
        
        # Obtener objetos del pool con timeout personalizable
        cuerpo = fabrica.get_cuerpo(timeout=timeout)
        montura = fabrica.get_montura(timeout=timeout)
        armadura = fabrica.get_armadura(timeout=timeout)
        arma = fabrica.get_arma(timeout=timeout)

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
            "pool_stats_before": fabrica.get_pool_stats(),
            "auto_return": auto_return,
            "timeout_used": timeout
        }

        # Devolver objetos al pool si auto_return está habilitado
        if auto_return:
            fabrica.devolver_cuerpo(cuerpo)
            fabrica.devolver_montura(montura)
            fabrica.devolver_armadura(armadura)
            fabrica.devolver_arma(arma)
            personaje_info["pool_stats_after"] = fabrica.get_pool_stats()
        else:
            personaje_info["warning"] = "Objetos no devueltos al pool. Usar /return/<kind> para devolverlos."

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


@bp.route("/pools/stats", methods=["GET"])
def get_all_pool_stats():
    """Obtiene estadísticas de todos los pools de fábricas"""
    all_stats = {}
    
    for factory_name, Factory in FACTORIES.items():
        # Crear instancia singleton (si ya existe, obtiene la misma)
        fabrica = Factory()
        all_stats[factory_name] = fabrica.get_pool_stats()
    
    return make_json_response({
        "message": "Estadísticas de pools de objetos (patrón Singleton + Pool)",
        "factories": all_stats
    })


@bp.route("/pools/<kind>/stats", methods=["GET"])
def get_factory_pool_stats(kind: str):
    """Obtiene estadísticas detalladas del pool de una fábrica específica"""
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    fabrica = Factory()
    stats = fabrica.get_pool_stats()
    
    return make_json_response({
        "factory": kind,
        "stats": stats,
        "explanation": {
            "singleton": "Esta fábrica usa patrón Singleton - siempre retorna la misma instancia",
            "object_pool": "Mantiene pools separados para reutilizar objetos de cada tipo",
            "pool_sizes": "Número de objetos disponibles en cada pool",
            "created_objects": "Número total de objetos creados desde el inicio"
        }
    })


@bp.route("/pools/<kind>/clear", methods=["POST"])
def clear_pool(kind: str):
    """Fuerza la limpieza de un pool específico"""
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    try:
        fabrica = Factory()
        stats_before = fabrica.get_pool_stats()
        
        # Limpiar todos los pools (simulado - en realidad solo vaciamos las queues)
        cleared_objects = {
            "cuerpos": fabrica._cuerpo_pool.qsize(),
            "monturas": fabrica._montura_pool.qsize(),
            "armaduras": fabrica._armadura_pool.qsize(),
            "armas": fabrica._arma_pool.qsize()
        }
        
        # Vaciar las queues
        while not fabrica._cuerpo_pool.empty():
            try: fabrica._cuerpo_pool.get_nowait()
            except: break
        while not fabrica._montura_pool.empty():
            try: fabrica._montura_pool.get_nowait()
            except: break
        while not fabrica._armadura_pool.empty():
            try: fabrica._armadura_pool.get_nowait()
            except: break
        while not fabrica._arma_pool.empty():
            try: fabrica._arma_pool.get_nowait()
            except: break
        
        stats_after = fabrica.get_pool_stats()
        
        return make_json_response({
            "message": f"Pool {kind} limpiado",
            "cleared_objects": cleared_objects,
            "stats_before": stats_before,
            "stats_after": stats_after
        })
        
    except Exception as e:
        return make_json_response({"error": str(e)}, status=500)


@bp.route("/pools/<kind>/reset", methods=["POST"])
def reset_pool_counters(kind: str):
    """Reinicia completamente los contadores de un pool (útil para testing)"""
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    try:
        fabrica = Factory()
        stats_before = fabrica.get_pool_stats()
        
        # Reset counters (esto es para testing, en producción podría no ser deseable)
        fabrica._created_cuerpos = 0
        fabrica._created_monturas = 0 
        fabrica._created_armaduras = 0
        fabrica._created_armas = 0
        
        # Clear pools
        while not fabrica._cuerpo_pool.empty():
            try: fabrica._cuerpo_pool.get_nowait()
            except: break
        while not fabrica._montura_pool.empty():
            try: fabrica._montura_pool.get_nowait()
            except: break
        while not fabrica._armadura_pool.empty():
            try: fabrica._armadura_pool.get_nowait()
            except: break
        while not fabrica._arma_pool.empty():
            try: fabrica._arma_pool.get_nowait()
            except: break
        
        stats_after = fabrica.get_pool_stats()
        
        return make_json_response({
            "message": f"Pool {kind} completamente reiniciado",
            "warning": "Esta operación reinicia contadores - solo para testing",
            "stats_before": stats_before,
            "stats_after": stats_after
        })
        
    except Exception as e:
        return make_json_response({"error": str(e)}, status=500)


@bp.route("/pools/<kind>/stress", methods=["POST"])
def stress_test_pool(kind: str):
    """Prueba de estrés del pool para demostrar límites"""
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    count = int(request.args.get('count', 5))
    timeout = int(request.args.get('timeout', 2))
    
    try:
        fabrica = Factory()
        initial_stats = fabrica.get_pool_stats()
        
        results = []
        objects_created = []
        
        # Intentar crear muchos objetos
        for i in range(count):
            try:
                start_time = time.time()
                cuerpo = fabrica.get_cuerpo(timeout=timeout)
                end_time = time.time()
                
                objects_created.append(cuerpo)
                stats = fabrica.get_pool_stats()
                
                results.append({
                    "iteration": i + 1,
                    "status": "success",
                    "time_ms": (end_time - start_time) * 1000,
                    "stats": stats
                })
                
            except RuntimeError as e:
                results.append({
                    "iteration": i + 1,
                    "status": "failed",
                    "error": str(e),
                    "stats": fabrica.get_pool_stats()
                })
                break
        
        # Devolver todos los objetos creados
        for obj in objects_created:
            fabrica.devolver_cuerpo(obj)
        
        final_stats = fabrica.get_pool_stats()
        
        return make_json_response({
            "message": f"Prueba de estrés completada para {kind}",
            "parameters": {"count": count, "timeout": timeout},
            "initial_stats": initial_stats,
            "results": results,
            "final_stats": final_stats,
            "objects_returned": len(objects_created)
        })
        
    except Exception as e:
        return make_json_response({"error": str(e)}, status=500)


@bp.route("/demo/singleton", methods=["GET"])
def demo_singleton_pattern():
    """Demuestra que las fábricas son singleton"""
    results = {}
    
    for factory_name, Factory in FACTORIES.items():
        # Crear múltiples "instancias" - todas deberían ser la misma
        fabrica1 = Factory()
        fabrica2 = Factory()
        fabrica3 = Factory()
        
        # Verificar que son la misma instancia
        same_instance = id(fabrica1) == id(fabrica2) == id(fabrica3)
        
        results[factory_name] = {
            "instance_id": id(fabrica1),
            "is_singleton": same_instance,
            "pool_stats": fabrica1.get_pool_stats()
        }
    
    return make_json_response({
        "message": "Demostración del patrón Singleton",
        "explanation": "Todas las 'instancias' de cada fábrica tienen el mismo ID, confirmando que es Singleton",
        "results": results
    })


@bp.route("/pools/limits", methods=["GET"])
def get_pool_limits():
    """Obtiene los límites configurados de todos los pools"""
    limits = {}
    
    for factory_name, Factory in FACTORIES.items():
        fabrica = Factory()
        limits[factory_name] = {
            "max_size": fabrica._max_size,
            "current_stats": fabrica.get_pool_stats()
        }
    
    return make_json_response({
        "message": "Límites de pools configurados",
        "limits": limits
    })


@bp.route("/pools/<kind>/config", methods=["GET", "POST"])
def pool_config(kind: str):
    """Obtiene o actualiza la configuración de un pool"""
    kind = kind.lower()
    Factory = FACTORIES.get(kind)
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    fabrica = Factory()
    
    if request.method == "GET":
        return make_json_response({
            "kind": kind,
            "max_size": fabrica._max_size,
            "stats": fabrica.get_pool_stats(),
            "instance_id": id(fabrica)
        })
    
    elif request.method == "POST":
        # Para actualizar configuración (limitado para seguridad)
        new_max_size = request.json.get('max_size') if request.is_json else None
        
        if new_max_size is not None and isinstance(new_max_size, int) and new_max_size > 0:
            old_max_size = fabrica._max_size
            fabrica._max_size = new_max_size
            
            return make_json_response({
                "message": f"Configuración de pool {kind} actualizada",
                "old_max_size": old_max_size,
                "new_max_size": new_max_size,
                "current_stats": fabrica.get_pool_stats(),
                "warning": "Cambio temporal - se reiniciará al restart del servidor"
            })
        else:
            return make_json_response({
                "error": "max_size debe ser un entero positivo",
                "example": {"max_size": 20}
            }, status=400)


@bp.route("/demo/pool-exhaustion", methods=["GET"])
def demo_pool_exhaustion():
    """Demuestra qué pasa cuando se agota el pool"""
    kind = request.args.get('kind', 'elfos')
    Factory = FACTORIES.get(kind)
    
    if not Factory:
        return make_json_response({"error": "Fabrica desconocida"}, status=404)
    
    try:
        fabrica = Factory()
        original_max_size = fabrica._max_size
        
        # Configurar límite pequeño para la demo
        fabrica._max_size = 2
        
        demo_results = []
        objects_held = []
        
        # Paso 1: Crear objetos hasta el límite
        demo_results.append({
            "step": 1,
            "description": "Creando objetos hasta el límite",
            "stats": fabrica.get_pool_stats()
        })
        
        for i in range(2):
            try:
                obj = fabrica.get_cuerpo(timeout=1)
                objects_held.append(obj)
                stats = fabrica.get_pool_stats()
                demo_results.append({
                    "step": f"1.{i+1}",
                    "description": f"Objeto {i+1} creado",
                    "stats": stats
                })
            except Exception as e:
                demo_results.append({
                    "step": f"1.{i+1}",
                    "description": f"Error creando objeto {i+1}",
                    "error": str(e)
                })
        
        # Paso 2: Intentar crear más objetos (debería fallar)
        demo_results.append({
            "step": 2,
            "description": "Intentando superar el límite (debería fallar)",
            "stats": fabrica.get_pool_stats()
        })
        
        try:
            obj = fabrica.get_cuerpo(timeout=1)
            demo_results.append({
                "step": "2.1",
                "description": "ERROR: No debería haber creado este objeto",
                "unexpected": True
            })
        except RuntimeError as e:
            demo_results.append({
                "step": "2.1", 
                "description": "Correcto: Pool exhausted como esperado",
                "error": str(e),
                "expected": True
            })
        
        # Paso 3: Devolver objetos y probar reutilización
        if objects_held:
            fabrica.devolver_cuerpo(objects_held[0])
            demo_results.append({
                "step": 3,
                "description": "Devolviendo 1 objeto al pool",
                "stats": fabrica.get_pool_stats()
            })
            
            try:
                obj = fabrica.get_cuerpo(timeout=1)
                demo_results.append({
                    "step": "3.1",
                    "description": "Éxito: Objeto reutilizado del pool",
                    "stats": fabrica.get_pool_stats()
                })
                fabrica.devolver_cuerpo(obj)
            except Exception as e:
                demo_results.append({
                    "step": "3.1",
                    "description": "Error inesperado al reutilizar",
                    "error": str(e)
                })
        
        # Limpiar
        for obj in objects_held[1:]:
            fabrica.devolver_cuerpo(obj)
        
        # Restaurar configuración original
        fabrica._max_size = original_max_size
        
        return make_json_response({
            "message": "Demostración de agotamiento de pool completada",
            "kind": kind,
            "demo_results": demo_results,
            "final_stats": fabrica.get_pool_stats(),
            "restored_max_size": original_max_size
        })
        
    except Exception as e:
        # Asegurar que restauramos la configuración
        if 'fabrica' in locals() and 'original_max_size' in locals():
            fabrica._max_size = original_max_size
        return make_json_response({"error": str(e)}, status=500)


def make_json_response(obj, status=200):
    """Serialize to JSON preserving unicode and ordering, set charset utf-8."""
    payload = json.dumps(obj, ensure_ascii=False, sort_keys=False)
    return Response(payload, status=status, mimetype='application/json; charset=utf-8')

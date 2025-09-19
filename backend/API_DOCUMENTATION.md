# Documentación de API - Fábrica de Personajes
## Patrón Singleton + Object Pool

### 📋 Índice
1. [Información General](#información-general)
2. [Rutas de Fábricas](#rutas-de-fábricas)
3. [Rutas de Gestión de Pools](#rutas-de-gestión-de-pools)
4. [Rutas de Estadísticas](#rutas-de-estadísticas)
5. [Rutas de Demostración](#rutas-de-demostración)
6. [Rutas de Imágenes](#rutas-de-imágenes)
7. [Códigos de Error](#códigos-de-error)
8. [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🌐 Información General

**Base URL:** `http://127.0.0.1:5000/api`

**Content-Type:** `application/json; charset=utf-8`

**Fábricas Disponibles:** `elfos`, `humanos`, `enanos`, `orcos`

---

## 🏭 Rutas de Fábricas

### `GET /factories`
**Descripción:** Lista todas las fábricas disponibles.

**Respuesta:**
```json
["elfos", "enanos", "humanos", "orcos"]
```

---

### `GET|POST /create/<kind>`
**Descripción:** Crea un personaje completo usando el patrón Singleton + Object Pool.

**Parámetros de Query:**
- `auto_return` (bool, default: true) - Si devolver automáticamente los objetos al pool
- `timeout` (int, default: 10) - Timeout en segundos para obtener objetos del pool

**Ejemplo:**
```bash
GET /api/create/elfos?auto_return=true&timeout=5
```

**Respuesta Exitosa (200):**
```json
{
  "status": "created",
  "kind": "elfos",
  "character": {
    "cuerpo": {
      "cuerpo_img": "/images/characters/elfo/elfo_cuerpo.png",
      "especie": "Elfo",
      "altura": "1.80m",
      "peso": "70kg",
      "habilidades": ["Visión nocturna", "Agilidad", "Magia"]
    },
    "montura": { ... },
    "armadura": { ... },
    "arma": { ... }
  },
  "pool_stats_before": {
    "cuerpo_pool_size": 0,
    "created_cuerpos": 1,
    ...
  },
  "pool_stats_after": {
    "cuerpo_pool_size": 1,
    "created_cuerpos": 1,
    ...
  },
  "auto_return": true,
  "timeout_used": 10
}
```

**Error Pool Exhausted (429):**
```json
{
  "error": "Pool exhausted",
  "message": "Pool exhausted: No hay objetos disponibles después de 10s. Creados: 10/10, Pool size: 0",
  "kind": "elfos",
  "pool_stats": { ... },
  "suggestion": "Usar /pools/elfos/clear o esperar a que se devuelvan objetos"
}
```

---

### `GET /character/<kind>/info`
**Descripción:** Obtiene información detallada de un personaje, devolviendo automáticamente los objetos al pool.

**Respuesta:**
```json
{
  "kind": "elfos",
  "cuerpo": { ... },
  "montura": { ... },
  "armadura": { ... },
  "arma": { ... },
  "pool_stats": { ... }
}
```

---

## 🏊 Rutas de Gestión de Pools

### `GET /pools/limits`
**Descripción:** Obtiene los límites configurados de todos los pools.

**Respuesta:**
```json
{
  "message": "Límites de pools configurados",
  "limits": {
    "elfos": {
      "max_size": 10,
      "current_stats": { ... }
    },
    "humanos": { ... },
    ...
  }
}
```

---

### `GET /pools/<kind>/config`
**Descripción:** Obtiene la configuración actual de un pool específico.

**Respuesta:**
```json
{
  "kind": "elfos",
  "max_size": 10,
  "stats": { ... },
  "instance_id": 2000906647312
}
```

---

### `POST /pools/<kind>/config`
**Descripción:** Actualiza la configuración de un pool (temporal, hasta restart del servidor).

**Body:**
```json
{
  "max_size": 15
}
```

**Respuesta:**
```json
{
  "message": "Configuración de pool elfos actualizada",
  "old_max_size": 10,
  "new_max_size": 15,
  "current_stats": { ... },
  "warning": "Cambio temporal - se reiniciará al restart del servidor"
}
```

---

### `POST /pools/<kind>/clear`
**Descripción:** Limpia todos los objetos disponibles en el pool (sin resetear contadores).

**Respuesta:**
```json
{
  "message": "Pool elfos limpiado",
  "cleared_objects": {
    "cuerpos": 3,
    "monturas": 2,
    "armaduras": 1,
    "armas": 4
  },
  "stats_before": { ... },
  "stats_after": { ... }
}
```

---

### `POST /pools/<kind>/reset`
**Descripción:** Reinicia completamente el pool y contadores (solo para testing).

**Respuesta:**
```json
{
  "message": "Pool elfos completamente reiniciado",
  "warning": "Esta operación reinicia contadores - solo para testing",
  "stats_before": { ... },
  "stats_after": { ... }
}
```

---

### `POST /pools/<kind>/stress`
**Descripción:** Ejecuta una prueba de estrés en el pool.

**Parámetros de Query:**
- `count` (int, default: 5) - Número de objetos a crear
- `timeout` (int, default: 2) - Timeout por objeto

**Ejemplo:**
```bash
POST /api/pools/elfos/stress?count=8&timeout=1
```

**Respuesta:**
```json
{
  "message": "Prueba de estrés completada para elfos",
  "parameters": {"count": 8, "timeout": 1},
  "initial_stats": { ... },
  "results": [
    {
      "iteration": 1,
      "status": "success",
      "time_ms": 0.5,
      "stats": { ... }
    },
    {
      "iteration": 6,
      "status": "failed",
      "error": "Pool exhausted: ...",
      "stats": { ... }
    }
  ],
  "final_stats": { ... },
  "objects_returned": 5
}
```

---

## 📊 Rutas de Estadísticas

### `GET /pools/stats`
**Descripción:** Obtiene estadísticas de todos los pools.

**Respuesta:**
```json
{
  "message": "Estadísticas de pools de objetos (patrón Singleton + Pool)",
  "factories": {
    "elfos": {
      "cuerpo_pool_size": 2,
      "montura_pool_size": 1,
      "armadura_pool_size": 0,
      "arma_pool_size": 3,
      "created_cuerpos": 5,
      "created_monturas": 3,
      "created_armaduras": 2,
      "created_armas": 7
    },
    ...
  }
}
```

---

### `GET /pools/<kind>/stats`
**Descripción:** Obtiene estadísticas detalladas de un pool específico.

**Respuesta:**
```json
{
  "factory": "elfos",
  "stats": {
    "cuerpo_pool_size": 2,
    "montura_pool_size": 1,
    "armadura_pool_size": 0,
    "arma_pool_size": 3,
    "created_cuerpos": 5,
    "created_monturas": 3,
    "created_armaduras": 2,
    "created_armas": 7
  },
  "explanation": {
    "singleton": "Esta fábrica usa patrón Singleton - siempre retorna la misma instancia",
    "object_pool": "Mantiene pools separados para reutilizar objetos de cada tipo",
    "pool_sizes": "Número de objetos disponibles en cada pool",
    "created_objects": "Número total de objetos creados desde el inicio"
  }
}
```

---

## 🎭 Rutas de Demostración

### `GET /demo/singleton`
**Descripción:** Demuestra que las fábricas implementan correctamente el patrón Singleton.

**Respuesta:**
```json
{
  "message": "Demostración del patrón Singleton",
  "explanation": "Todas las 'instancias' de cada fábrica tienen el mismo ID, confirmando que es Singleton",
  "results": {
    "elfos": {
      "instance_id": 2000906647312,
      "is_singleton": true,
      "pool_stats": { ... }
    },
    ...
  }
}
```

---

### `GET /demo/pool-exhaustion`
**Descripción:** Demuestra paso a paso qué ocurre cuando se agota un pool.

**Parámetros de Query:**
- `kind` (string, default: "elfos") - Tipo de fábrica para la demo

**Ejemplo:**
```bash
GET /api/demo/pool-exhaustion?kind=humanos
```

**Respuesta:**
```json
{
  "message": "Demostración de agotamiento de pool completada",
  "kind": "elfos",
  "demo_results": [
    {
      "step": 1,
      "description": "Creando objetos hasta el límite",
      "stats": { ... }
    },
    {
      "step": "2.1",
      "description": "Correcto: Pool exhausted como esperado",
      "error": "Pool exhausted: No hay objetos disponibles...",
      "expected": true
    },
    {
      "step": "3.1",
      "description": "Éxito: Objeto reutilizado del pool",
      "stats": { ... }
    }
  ],
  "final_stats": { ... },
  "restored_max_size": 10
}
```

---

## 🖼️ Rutas de Imágenes

### `GET /images/<category>`
**Descripción:** Lista todas las imágenes de una categoría.

**Categorías:** `characters`, `avatars`, `ui`

**Respuesta:**
```json
{
  "category": "characters",
  "images": [
    "/images/characters/elfo/elfo_cuerpo.png",
    "/images/characters/humano/humano_cuerpo.png",
    ...
  ]
}
```

---

### `GET /images/<category>/<filename>`
**Descripción:** Sirve una imagen específica.

**Ejemplo:**
```bash
GET /api/images/characters/elfo/elfo_cuerpo.png
```

---

### `POST /upload/<category>`
**Descripción:** Sube una nueva imagen.

**Body:** `multipart/form-data` con campo `image`

**Respuesta:**
```json
{
  "message": "Image uploaded successfully",
  "path": "/images/characters/nuevo_personaje.png"
}
```

---

## ⚠️ Códigos de Error

| Código | Descripción | Causa Común |
|--------|-------------|-------------|
| **200** | OK | Operación exitosa |
| **400** | Bad Request | Parámetros inválidos o categoría no válida |
| **404** | Not Found | Fábrica desconocida o imagen no encontrada |
| **429** | Too Many Requests | Pool exhausted - límite alcanzado |
| **500** | Internal Server Error | Error interno del servidor |

---

## 📝 Ejemplos de Uso

### Ejemplo 1: Crear personaje y monitorear pool
```python
import requests

# 1. Ver estado inicial
response = requests.get('http://127.0.0.1:5000/api/pools/elfos/stats')
print(f"Estado inicial: {response.json()['stats']}")

# 2. Crear personaje
response = requests.get('http://127.0.0.1:5000/api/create/elfos?auto_return=false')
personaje = response.json()
print(f"Personaje creado: {personaje['character']['cuerpo']['especie']}")

# 3. Ver estado después
response = requests.get('http://127.0.0.1:5000/api/pools/elfos/stats')
print(f"Estado después: {response.json()['stats']}")
```

### Ejemplo 2: Prueba de límites
```python
import requests

# 1. Configurar límite pequeño para prueba
requests.post('http://127.0.0.1:5000/api/pools/elfos/config', 
              json={"max_size": 2})

# 2. Crear objetos hasta límite
for i in range(3):
    try:
        response = requests.get('http://127.0.0.1:5000/api/create/elfos?auto_return=false&timeout=1')
        if response.status_code == 429:
            print(f"Pool exhausted en iteración {i+1}")
            break
        else:
            print(f"Objeto {i+1} creado")
    except Exception as e:
        print(f"Error: {e}")

# 3. Limpiar y restaurar
requests.post('http://127.0.0.1:5000/api/pools/elfos/reset')
requests.post('http://127.0.0.1:5000/api/pools/elfos/config', 
              json={"max_size": 10})
```

### Ejemplo 3: Demostración completa
```python
import requests

# Demo singleton
response = requests.get('http://127.0.0.1:5000/api/demo/singleton')
singleton_demo = response.json()
print(f"Singleton demo: {singleton_demo['message']}")

# Demo pool exhaustion  
response = requests.get('http://127.0.0.1:5000/api/demo/pool-exhaustion?kind=elfos')
exhaustion_demo = response.json()
print(f"Exhaustion demo: {exhaustion_demo['message']}")

# Prueba de estrés
response = requests.post('http://127.0.0.1:5000/api/pools/elfos/stress?count=5&timeout=2')
stress_test = response.json()
print(f"Stress test: {stress_test['message']}")
```

---

## 🔧 Notas Técnicas

### Parámetros del Object Pool
- **max_size**: Número máximo de objetos que se pueden crear por tipo
- **timeout**: Tiempo máximo a esperar por un objeto del pool
- **auto_return**: Si devolver automáticamente objetos al pool después de uso

### Comportamiento del Pool
1. **Dentro del límite**: Crea nuevos objetos normalmente
2. **Límite alcanzado + pool disponible**: Reutiliza objetos del pool
3. **Límite alcanzado + pool vacío**: Espera con timeout o error 429

### Thread Safety
- Todos los pools son thread-safe
- Singleton implementa double-checked locking
- Safe para entornos de producción concurrentes

---

**Versión:** 1.0  
**Fecha:** Septiembre 2025  
**Patrón:** Singleton + Object Pool  
**Framework:** Flask + Python 3.11+
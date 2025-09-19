# API Quick Reference - Fábrica de Personajes

## 🚀 Base URL
```
http://127.0.0.1:5000/api
```

## 📋 Rutas Principales

### Fábricas
```bash
GET  /factories                          # Lista fábricas disponibles
GET  /create/{kind}                      # Crear personaje (elfos|humanos|enanos|orcos)
GET  /character/{kind}/info              # Info de personaje
```

### Pools - Estadísticas
```bash
GET  /pools/stats                        # Stats de todos los pools
GET  /pools/{kind}/stats                 # Stats de pool específico
GET  /pools/limits                       # Límites configurados
```

### Pools - Gestión
```bash
GET  /pools/{kind}/config                # Ver configuración
POST /pools/{kind}/config                # Cambiar configuración
POST /pools/{kind}/clear                 # Limpiar pool
POST /pools/{kind}/reset                 # Reset completo (testing)
POST /pools/{kind}/stress                # Prueba de estrés
```

### Demostraciones
```bash
GET  /demo/singleton                     # Demo patrón Singleton
GET  /demo/pool-exhaustion               # Demo agotamiento pool
```

### Imágenes
```bash
GET  /images/{category}                  # Lista imágenes (characters|avatars|ui)
GET  /images/{category}/{filename}       # Servir imagen
POST /upload/{category}                  # Subir imagen
```

## 🔧 Parámetros Comunes

### Query Parameters
```bash
?auto_return=true|false                  # Auto devolver al pool (default: true)
?timeout=10                              # Timeout en segundos (default: 10)
?count=5                                 # Número de objetos para stress test
?kind=elfos                              # Tipo de fábrica para demos
```

### Request Body (POST config)
```json
{
  "max_size": 15                         # Nuevo límite del pool
}
```

## 📊 Respuestas Típicas

### Crear Personaje (200)
```json
{
  "status": "created",
  "kind": "elfos",
  "character": { "cuerpo": {...}, "montura": {...}, ... },
  "pool_stats_before": {...},
  "pool_stats_after": {...},
  "auto_return": true
}
```

### Pool Exhausted (429)
```json
{
  "error": "Pool exhausted",
  "message": "No hay objetos disponibles después de 10s...",
  "suggestion": "Usar /pools/{kind}/clear o esperar..."
}
```

### Stats de Pool (200)
```json
{
  "stats": {
    "cuerpo_pool_size": 2,
    "created_cuerpos": 5,
    "montura_pool_size": 1,
    "created_monturas": 3,
    ...
  }
}
```

## ⚡ Ejemplos Rápidos

### Python + requests
```python
import requests

BASE = "http://127.0.0.1:5000/api"

# Crear elfo
r = requests.get(f"{BASE}/create/elfos")

# Ver stats
r = requests.get(f"{BASE}/pools/elfos/stats")

# Demo singleton
r = requests.get(f"{BASE}/demo/singleton")

# Prueba de estrés
r = requests.post(f"{BASE}/pools/elfos/stress?count=5")
```

### curl
```bash
# Crear personaje
curl -X GET "http://127.0.0.1:5000/api/create/elfos?auto_return=true"

# Ver límites
curl -X GET "http://127.0.0.1:5000/api/pools/limits"

# Cambiar configuración
curl -X POST "http://127.0.0.1:5000/api/pools/elfos/config" \
     -H "Content-Type: application/json" \
     -d '{"max_size": 15}'

# Demo agotamiento
curl -X GET "http://127.0.0.1:5000/api/demo/pool-exhaustion?kind=elfos"
```

## 🚨 Códigos de Estado

| Código | Significado |
|--------|-------------|
| 200 | ✅ OK |
| 400 | ❌ Bad Request (parámetros inválidos) |
| 404 | ❌ Not Found (fábrica desconocida) |
| 429 | ⚠️ Pool Exhausted (límite alcanzado) |
| 500 | 💥 Internal Error |

## 🎯 Casos de Uso

### Testing Pool Limits
1. `POST /pools/{kind}/config` → Configurar límite pequeño
2. `GET /create/{kind}?auto_return=false` → Crear hasta límite
3. Observar error 429 cuando se agote
4. `POST /pools/{kind}/clear` → Limpiar para continuar

### Monitoreo Producción
1. `GET /pools/stats` → Ver estado general
2. `GET /pools/limits` → Verificar configuración
3. `GET /demo/singleton` → Validar instancias únicas

### Performance Testing
1. `POST /pools/{kind}/stress?count=20&timeout=1` → Stress test
2. Analizar resultados y tiempos de respuesta
3. `POST /pools/{kind}/reset` → Limpiar después de test

---
**Tip:** Usar `auto_return=true` (default) para uso normal, `auto_return=false` para testing de límites.
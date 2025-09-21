# API Quick Reference - Fábrica de Personajes
## ✨ Rutas Actuales Implementadas

### 🚀 Base URL
```
http://127.0.0.1:5000/api
```

## 📋 Endpoints Disponibles

### 🏭 Fábricas Básicas
```bash
GET  /factories                          # Lista todas las fábricas disponibles
GET  /create/{kind}                      # Crear personaje completo (elfos|humanos|enanos|orcos)  
GET  /character/{kind}/info              # Información detallada de un personaje
```

### 🔄 Pool Singleton - Gestión
```bash
GET    /pool/status                      # Estado actual del pool singleton global
DELETE /pool/delete/{kind}               # Eliminar fábrica específica (solo si coincide)
POST   /pool/delete/{kind}               # Eliminar fábrica específica (método POST)
DELETE /pool/force-clear                 # Limpiar pool forzadamente (⚠️ sin validación)
POST   /pool/force-clear                 # Limpiar pool forzadamente (método POST)
```

### 🖼️ Gestión de Imágenes
```bash
GET  /images/{category}                  # Lista imágenes por categoría (characters|avatars|ui)
GET  /images/{category}/{filename}       # Servir imagen específica
POST /upload/{category}                  # Subir nueva imagen a categoría
```

## 🔧 Parámetros Principales

### Query Parameters - /create/{kind}
```bash
?auto_return=true|false                  # Auto devolver objetos al pool (default: true)
?timeout=10                              # Timeout en segundos (default: 10)
?delete=true                             # Eliminar fábrica en lugar de crear personaje
```

### Request Body - /upload/{category}
```bash
Content-Type: multipart/form-data
Campo: "image" (archivo)
Extensiones: .png, .jpg, .jpeg, .gif, .svg, .webp
```

## 📊 Respuestas Típicas

### ✅ Crear Personaje (200)
```json
{
  "status": "created",
  "kind": "elfos",
  "character": {
    "cuerpo": { "cuerpo_img": "...", "especie": "Elfo", ... },
    "montura": { "tipo": "Caballo élfico", ... },
    "armadura": { "tipo": "Armadura élfica", ... },
    "arma": { "tipo": "Arco élfico", ... }
  }
}
```

### 📊 Pool Status (200)
```json
{
  "has_factory": true,
  "factory_type": "FabricarElfos",
  "factory_instance": "<app.factories.elfos.FabricarElfos object at 0x...>"
}
```

### ✅ Eliminación Exitosa (200)
```json
{
  "message": "Fabrica 'elfos' eliminada del pool exitosamente",
  "deleted_factory": "elfos",
  "previous_factory": { ... },
  "success": true
}
```

### ❌ Error - Fábrica Diferente (400)
```json
{
  "error": "No se puede eliminar la fábrica",
  "message": "La fábrica actual en el pool es 'FabricarHumanos', no se puede eliminar 'elfos'",
  "current_factory": { ... },
  "requested_deletion": "elfos",
  "success": false
}
```

### ❌ Fábrica Desconocida (404)
```json
{
  "error": "Fabrica desconocida"
}
```

### ❌ Error Interno (500)
```json
{
  "error": "Internal error",
  "message": "Descripción del error...",
  "kind": "elfos"
}
```

## ⚡ Ejemplos de Uso

### Python + requests
```python
import requests

BASE = "http://127.0.0.1:5000/api"

# 1. Ver qué fábrica está en el pool
status = requests.get(f"{BASE}/pool/status")
print(status.json())

# 2. Crear un elfo
elfo = requests.get(f"{BASE}/create/elfos")
print(elfo.json())

# 3. Eliminar la fábrica de elfos del pool
delete_result = requests.delete(f"{BASE}/pool/delete/elfos")
print(delete_result.json())

# 4. Intentar eliminar otra fábrica (fallará)
delete_humanos = requests.delete(f"{BASE}/pool/delete/humanos")
print(delete_humanos.json())  # Error 400

# 5. Limpiar forzadamente
force_clear = requests.delete(f"{BASE}/pool/force-clear")
print(force_clear.json())
```

### curl - Casos de Uso
```bash
# Ver estado del pool
curl -X GET "http://127.0.0.1:5000/api/pool/status"

# Crear personaje con parámetros
curl -X GET "http://127.0.0.1:5000/api/create/elfos?auto_return=true&timeout=5"

# Eliminar fábrica específica
curl -X DELETE "http://127.0.0.1:5000/api/pool/delete/elfos"

# Alternativamente, eliminar vía query param
curl -X GET "http://127.0.0.1:5000/api/create/elfos?delete=true"

# Limpiar pool forzadamente
curl -X DELETE "http://127.0.0.1:5000/api/pool/force-clear"

# Listar imágenes
curl -X GET "http://127.0.0.1:5000/api/images/characters"

# Subir imagen
curl -X POST "http://127.0.0.1:5000/api/upload/characters" \
     -F "image=@mi_imagen.png"
```

## 🚨 Códigos de Estado HTTP

| Código | Descripción | Cuando Ocurre |
|--------|-------------|---------------|
| 200 | ✅ OK | Operación exitosa |
| 400 | ❌ Bad Request | Parámetros inválidos, fábrica incorrecta para eliminar |
| 404 | ❌ Not Found | Fábrica desconocida, imagen no encontrada |
| 500 | 💥 Internal Error | Error del servidor |

## 🎯 Casos de Uso Reales

### 🔄 Cambiar de Fábrica
```python
# Paso 1: Ver qué hay en el pool
status = requests.get(f"{BASE}/pool/status")

# Paso 2: Si hay una fábrica diferente, eliminarla
if status.json()['has_factory']:
    current_type = status.json()['factory_type']
    if 'Elfos' in current_type:
        requests.delete(f"{BASE}/pool/delete/elfos")

# Paso 3: Crear nueva fábrica
humano = requests.get(f"{BASE}/create/humanos")
```

### 🧪 Testing de Pool Singleton
```python
# Verificar que el patrón Singleton funciona
elfo1 = requests.get(f"{BASE}/create/elfos")
elfo2 = requests.get(f"{BASE}/create/elfos")

# Ambos deberían usar la misma instancia de fábrica
# El pool mantiene una única instancia por tipo
```

### 🛠️ Mantenimiento del Pool
```python
# Limpiar completamente el pool para empezar fresh
requests.delete(f"{BASE}/pool/force-clear")

# Verificar que está limpio
status = requests.get(f"{BASE}/pool/status")
assert not status.json()['has_factory']
```

---

**💡 Tip:** Usa `/pool/status` antes de operaciones para entender el estado actual del sistema.

**⚠️ Precaución:** `/pool/force-clear` elimina cualquier fábrica sin validación. Úsalo solo cuando sea necesario.

**🔍 Debug:** Si una operación falla, revisa el `status` y los `factory_type` para entender qué fábrica está activa.
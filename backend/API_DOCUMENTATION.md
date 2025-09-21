# Documentación Completa de API - Fábrica de Personajes
## 🏗️ Sistema con Patrón Singleton + Object Pool

### 📚 Índice
1. [Información General](#información-general)
2. [Rutas de Fábricas](#rutas-de-fábricas)
3. [Rutas de Pool Singleton](#rutas-de-pool-singleton)
4. [Rutas de Imágenes](#rutas-de-imágenes)
5. [Códigos de Error](#códigos-de-error)
6. [Arquitectura Técnica](#arquitectura-técnica)
7. [Ejemplos Avanzados](#ejemplos-avanzados)

---

## 🌐 Información General

**Base URL:** `http://127.0.0.1:5000/api`

**Content-Type:** `application/json; charset=utf-8`

**Fábricas Disponibles:** `elfos`, `humanos`, `enanos`, `orcos`

**Patrones Implementados:**
- **Singleton Pattern**: Una única instancia de fábrica por tipo
- **Object Pool Pattern**: Reutilización de objetos para optimizar memoria
- **Factory Pattern**: Creación centralizada de objetos por especie

---

## 🏭 Rutas de Fábricas

### `GET /factories`
**Descripción:** Lista todas las fábricas de personajes disponibles en el sistema.

**Respuesta (200):**
```json
["elfos", "enanos", "humanos", "orcos"]
```

**Ejemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/api/factories"
```

---

### `GET|POST /create/<kind>`
**Descripción:** Crea un personaje completo usando el patrón Singleton + Object Pool. La fábrica se mantiene como singleton y los objetos se reutilizan.

**Parámetros de Path:**
- `kind`: Tipo de personaje (`elfos`, `humanos`, `enanos`, `orcos`)

**Parámetros de Query:**
- `auto_return` (bool, default: true) - Si devolver automáticamente los objetos al pool
- `timeout` (int, default: 10) - Timeout en segundos para obtener objetos del pool
- `delete` (bool) - Si es "true", elimina la fábrica del pool en lugar de crear personaje

**Ejemplos:**
```bash
# Crear personaje elfo
GET /api/create/elfos?auto_return=true&timeout=5

# Eliminar fábrica del pool
GET /api/create/elfos?delete=true

# Crear sin auto-return (para testing)
GET /api/create/elfos?auto_return=false
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
    "montura": {
      "imagen": "/images/characters/elfo_montura.png",
      "tipo": "Caballo élfico",
      "velocidad": "Muy rápida",
      "habilidades": ["Vuelo corto", "Salto alto"]
    },
    "armadura": {
      "imagen": "/images/characters/elfo_armadura.png",
      "tipo": "Armadura élfica",
      "material": "Mithril",
      "defensa": "Alta",
      "peso": "Ligera"
    },
    "arma": {
      "imagen": "/images/characters/elfo_arma.png",
      "tipo": "Arco élfico",
      "material": "Madera sagrada",
      "daño": "Alto",
      "alcance": "Largo"
    }
  }
}
```

**Respuesta con delete=true (200):**
```json
{
  "message": "Fabrica 'elfos' eliminada del pool exitosamente",
  "deleted_factory": "elfos",
  "previous_factory": {
    "has_factory": true,
    "factory_type": "FabricarElfos",
    "factory_instance": "<app.factories.elfos.FabricarElfos object at 0x...>"
  }
}
```

**Error - Fábrica Desconocida (404):**
```json
{
  "error": "Fabrica desconocida"
}
```

**Error - No se puede eliminar (400):**
```json
{
  "error": "No se puede eliminar la fábrica",
  "message": "La fábrica actual en el pool es 'FabricarHumanos', no se puede eliminar 'elfos'",
  "current_factory": { ... },
  "requested_deletion": "elfos",
  "success": false
}
```

---

### `GET /character/<kind>/info`
**Descripción:** Obtiene información detallada de un personaje. Crea temporalmente los objetos y los devuelve automáticamente al pool.

**Respuesta (200):**
```json
{
  "kind": "elfos",
  "cuerpo": { ... },
  "montura": { ... },
  "armadura": { ... },
  "arma": { ... }
}
```

---

## 🔄 Rutas de Pool Singleton

### `GET /pool/status`
**Descripción:** Obtiene el estado actual del pool singleton global. Muestra qué fábrica está actualmente cargada.

**Respuesta (200):**
```json
{
  "has_factory": true,
  "factory_type": "FabricarElfos",
  "factory_instance": "<app.factories.elfos.FabricarElfos object at 0x1a2b3c4d>"
}
```

**Respuesta - Pool vacío (200):**
```json
{
  "has_factory": false,
  "factory_type": null,
  "factory_instance": null
}
```

**Ejemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/api/pool/status"
```

---

### `DELETE|POST /pool/delete/<kind>`
**Descripción:** Elimina una fábrica específica del pool singleton. **Solo permite eliminar si es exactamente la misma fábrica que está actualmente en uso.**

**Parámetros de Path:**
- `kind`: Tipo de fábrica a eliminar (`elfos`, `humanos`, `enanos`, `orcos`)

**Comportamiento:**
- ✅ **Permite eliminación**: Si la fábrica actual coincide con `kind`
- ❌ **Rechaza eliminación**: Si hay una fábrica diferente en el pool
- ✅ **Permite eliminación**: Si el pool está vacío (no hay fábrica)

**Respuesta Exitosa (200):**
```json
{
  "message": "Fabrica 'elfos' eliminada del pool exitosamente",
  "deleted_factory": "elfos",
  "previous_factory": {
    "has_factory": true,
    "factory_type": "FabricarElfos",
    "factory_instance": "<...>"
  },
  "success": true
}
```

**Error - Fábrica Diferente (400):**
```json
{
  "error": "No se puede eliminar la fábrica",
  "message": "La fábrica actual en el pool es 'FabricarHumanos', no se puede eliminar 'elfos'",
  "current_factory": {
    "has_factory": true,
    "factory_type": "FabricarHumanos",
    "factory_instance": "<...>"
  },
  "requested_deletion": "elfos",
  "success": false
}
```

**Ejemplos:**
```bash
# Eliminar fábrica de elfos (solo si está activa)
curl -X DELETE "http://127.0.0.1:5000/api/pool/delete/elfos"

# Método POST alternativo
curl -X POST "http://127.0.0.1:5000/api/pool/delete/elfos"
```

---

### `DELETE|POST /pool/force-clear`
**Descripción:** Fuerza la eliminación de cualquier fábrica del pool sin validación de tipo. ⚠️ **Usar con precaución** - elimina cualquier fábrica sin importar el tipo.

**Comportamiento:**
- Elimina cualquier fábrica que esté en el pool
- No valida el tipo de fábrica
- Útil para limpieza de testing o reseteo del sistema

**Respuesta (200):**
```json
{
  "message": "Pool limpiado forzadamente",
  "previous_factory": {
    "has_factory": true,
    "factory_type": "FabricarElfos",
    "factory_instance": "<...>"
  },
  "success": true,
  "warning": "Se eliminó cualquier fábrica sin validación de tipo"
}
```

**Ejemplo:**
```bash
curl -X DELETE "http://127.0.0.1:5000/api/pool/force-clear"
```

---

## 🖼️ Rutas de Imágenes

### `GET /images/<category>`
**Descripción:** Lista todas las imágenes disponibles en una categoría específica.

**Parámetros de Path:**
- `category`: Categoría de imagen (`characters`, `avatars`, `ui`)

**Respuesta (200):**
```json
{
  "category": "characters",
  "images": [
    "/images/characters/elfo/elfo_cuerpo.png",
    "/images/characters/enano/enano_cuerpo.png",
    "/images/characters/humano/humano_cuerpo.png",
    ...
  ]
}
```

**Error - Categoría inválida (400):**
```json
{
  "error": "Invalid category"
}
```

---

### `GET /images/<category>/<filename>`
**Descripción:** Sirve una imagen específica directamente.

**Parámetros de Path:**
- `category`: Categoría de imagen
- `filename`: Nombre del archivo de imagen

**Respuesta (200):** Archivo de imagen (binary content)

**Error - Imagen no encontrada (404):**
```json
{
  "error": "Image not found"
}
```

**Ejemplo:**
```bash
curl -X GET "http://127.0.0.1:5000/api/images/characters/elfo/elfo_cuerpo.png"
```

---

### `POST /upload/<category>`
**Descripción:** Sube una nueva imagen a una categoría específica.

**Parámetros de Path:**
- `category`: Categoría destino (`characters`, `avatars`, `ui`)

**Request Body:**
```
Content-Type: multipart/form-data
Campo: "image" (archivo)
```

**Extensiones permitidas:** `.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.webp`

**Respuesta Exitosa (200):**
```json
{
  "message": "Image uploaded successfully",
  "path": "/images/characters/mi_nueva_imagen.png"
}
```

**Errores:**
- **400**: No se proporcionó archivo, nombre vacío, extensión inválida
- **500**: Error interno al guardar

**Ejemplo:**
```bash
curl -X POST "http://127.0.0.1:5000/api/upload/characters" \
     -F "image=@mi_imagen.png"
```

---

## 🚨 Códigos de Error Completos

| Código | Descripción | Casos Típicos |
|--------|-------------|---------------|
| **200** | ✅ OK | Operación exitosa, datos válidos |
| **400** | ❌ Bad Request | Fábrica incorrecta para eliminar, categoría inválida, archivo inválido |
| **404** | ❌ Not Found | Fábrica desconocida, imagen no encontrada |
| **500** | 💥 Internal Error | Error del servidor, problema al crear objetos |

---

## 🏗️ Arquitectura Técnica

### Patrón Singleton
- **Una instancia por tipo**: Solo existe una instancia de `FabricarElfos`, `FabricarHumanos`, etc.
- **Pool global**: Un singleton global `Pool` gestiona qué fábrica está activa
- **Thread-safe**: Implementación segura para concurrencia

### Validación de Eliminación
```python
# Solo permite eliminar si el tipo coincide
if self._factory_type == factory_class:
    self._factory = None
    self._factory_type = None
    return True
else:
    return False  # Fábrica diferente - no se puede eliminar
```

### Factory Pattern
- **Interfaces comunes**: `ICuerpo`, `IMontura`, `IArmadura`, `IArma`
- **Implementación específica**: Cada raza implementa sus propias versiones
- **Creación centralizada**: Métodos `crear_*` en cada fábrica

---

## 📖 Ejemplos Avanzados

### Flujo Completo: Cambio de Fábrica
```python
import requests

BASE = "http://127.0.0.1:5000/api"

# 1. Verificar estado actual
status = requests.get(f"{BASE}/pool/status")
print(f"Estado inicial: {status.json()}")

# 2. Crear personaje elfo (carga FabricarElfos)
elfo = requests.get(f"{BASE}/create/elfos")
print(f"Elfo creado: {elfo.json()['status']}")

# 3. Verificar que la fábrica cambió
status = requests.get(f"{BASE}/pool/status")
print(f"Fábrica actual: {status.json()['factory_type']}")

# 4. Intentar eliminar fábrica incorrecta (fallará)
delete_humanos = requests.delete(f"{BASE}/pool/delete/humanos")
print(f"Eliminar humanos: {delete_humanos.status_code} - {delete_humanos.json()['error']}")

# 5. Eliminar fábrica correcta (exitoso)
delete_elfos = requests.delete(f"{BASE}/pool/delete/elfos")
print(f"Eliminar elfos: {delete_elfos.json()['success']}")

# 6. Crear humano (carga FabricarHumanos)
humano = requests.get(f"{BASE}/create/humanos")
print(f"Humano creado: {humano.json()['status']}")
```

### Testing de Validación
```python
# Caso 1: Pool vacío - cualquier eliminación falla
requests.delete(f"{BASE}/pool/force-clear")
result = requests.delete(f"{BASE}/pool/delete/elfos")
# result.json()['success'] == False (no hay fábrica que eliminar)

# Caso 2: Fábrica correcta - eliminación exitosa  
requests.get(f"{BASE}/create/elfos")
result = requests.delete(f"{BASE}/pool/delete/elfos")
# result.json()['success'] == True

# Caso 3: Fábrica incorrecta - eliminación rechazada
requests.get(f"{BASE}/create/elfos")
result = requests.delete(f"{BASE}/pool/delete/humanos")
# result.status_code == 400, result.json()['success'] == False
```

### Mantenimiento del Sistema
```python
# Limpiar completamente para testing
requests.delete(f"{BASE}/pool/force-clear")

# Verificar limpieza
status = requests.get(f"{BASE}/pool/status")
assert not status.json()['has_factory']

# Cargar fábrica específica
requests.get(f"{BASE}/create/elfos")

# Verificar carga
status = requests.get(f"{BASE}/pool/status")
assert status.json()['factory_type'] == 'FabricarElfos'
```

---

**💡 Notas Importantes:**

1. **Singleton por Tipo**: Cada tipo de fábrica mantiene su propia instancia singleton
2. **Pool Global**: Solo una fábrica puede estar activa a la vez en el pool global
3. **Validación Estricta**: No se puede eliminar una fábrica de diferente tipo
4. **Force Clear**: Úsalo solo para testing o reseteo completo del sistema
5. **Thread Safety**: El sistema está diseñado para ser thread-safe
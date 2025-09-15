import os
import json
from pathlib import Path

class ImagePathManager:
    """Maneja las rutas de imágenes compartidas entre frontend y backend"""
    
    def __init__(self):
        # Intentar detectar la raíz del proyecto buscando shared-config.json o la carpeta 'public'
        candidate = Path(__file__).parent.parent.parent
        # Subir hasta 4 niveles buscando pistas de raíz
        for _ in range(5):
            if (candidate / 'shared-config.json').exists() or (candidate / 'public').exists():
                break
            if candidate.parent == candidate:
                break
            candidate = candidate.parent

        self.project_root = candidate
        self.config_path = self.project_root / "shared-config.json"
        self.config = self._load_config()
    
    def _load_config(self):
        """Carga la configuración compartida"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "paths": {
                    "images": {
                        "root": "./public/images",
                        "characters": "./public/images/characters",
                        "avatars": "./public/images/avatars",
                        "ui": "./public/images/ui"
                    }
                }
            }
    
    def get_image_path(self, category: str, filename: str = None):
        """
        Obtiene la ruta completa de una imagen
        
        Args:
            category: 'characters', 'avatars', 'ui'
            filename: nombre del archivo (opcional)
        
        Returns:
            Path completo de la imagen
        """
        # Leer rutas desde el config si existe, sino usar convención por defecto
        try:
            paths = self.config.get('paths', {}).get('images', {})
            category_map = {
                'characters': paths.get('characters', './public/images/characters'),
                'avatars': paths.get('avatars', './public/images/avatars'),
                'ui': paths.get('ui', './public/images/ui'),
            }
            rel = category_map.get(category)
            if rel is None:
                # Fallback: asumir carpeta dentro de public/images
                rel = f'./public/images/{category}'
        except Exception:
            rel = f'./public/images/{category}'

        base_path = (self.project_root / rel).resolve()
        if filename:
            return base_path / filename
        return base_path
    
    def get_web_path(self, category: str, filename: str):
        """
        Obtiene la ruta web para usar en el frontend
        
        Args:
            category: 'characters', 'avatars', 'ui'
            filename: nombre del archivo
        
        Returns:
            Ruta web (ej: '/images/characters/elfo.png')
        """
        # Soportar filename con subdirectorios y normalizar separadores
        # filename puede ser 'personajes/elfo/imagen.png' o Path
        if isinstance(filename, Path):
            path = filename.as_posix()
        else:
            path = str(filename).replace('\\', '/').lstrip('/')

        # Verificar existencia en disco: si no existe, devolver None (la clase debe encargarse)
        try:
            fs_path = self.get_image_path(category, path)
            if not fs_path.exists():
                return None
        except Exception:
            # Si hay algún error al resolver la ruta, devolver None
            return None

        return f"/images/{category}/{path}"
    
    def save_image(self, category: str, filename: str, file_data):
        """
        Guarda una imagen en la carpeta correspondiente
        
        Args:
            category: 'characters', 'avatars', 'ui'
            filename: nombre del archivo
            file_data: datos del archivo
        """
        image_path = self.get_image_path(category, filename)
        image_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(image_path, 'wb') as f:
            f.write(file_data)
        
        return self.get_web_path(category, filename)
    
    def list_images(self, category: str):
        """
        Lista todas las imágenes de una categoría
        
        Args:
            category: 'characters', 'avatars', 'ui'
        
        Returns:
            Lista de nombres de archivos
        """
        path = self.get_image_path(category)
        if path.exists():
            return [f.name for f in path.iterdir() if f.is_file()]
        return []

    # Helpers específicos para 'characters' con subcarpetas tipo 'personajes/<clase>/<personaje>'
    def _characters_base(self):
        """Devuelve el directorio base de characters (respetando posible subfolder 'personajes')."""
        base = self.get_image_path('characters')
        # Si hay una carpeta 'personajes' dentro, usarla
        p = base / 'personajes'
        if p.exists() and p.is_dir():
            return p
        return base

    def list_classes(self):
        """Lista las 'clases' (ej: elfo, enano) dentro de characters/personajes o characters."""
        base = self._characters_base()
        if not base.exists():
            return []
        return [d.name for d in base.iterdir() if d.is_dir()]

    def list_characters(self, class_name: str):
        """Lista carpetas de personajes dentro de una clase específica.

        Args:
            class_name: nombre de la clase (ej: 'elfo')
        Returns:
            lista de nombres de carpetas de personajes
        """
        base = self._characters_base() / class_name
        if not base.exists() or not base.is_dir():
            return []
        return [d.name for d in base.iterdir() if d.is_dir()]

    def get_character_image_path(self, class_name: str, character_folder: str, filename: str = None):
        """Construye la ruta a una imagen de personaje dada su clase y carpeta.

        Ejemplo: class_name='elfo', character_folder='elfo_avatar', filename='img.png'
        -> .../public/images/characters/personajes/elfo/elfo_avatar/img.png
        """
        base = self._characters_base() / class_name / character_folder
        if filename:
            return (base / filename).resolve()
        return base.resolve()

# Instancia global
image_manager = ImagePathManager()

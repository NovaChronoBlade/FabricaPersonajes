class FactoryYaExiste(Exception):
    """Excepción lanzada cuando se intenta crear una fábrica que ya existe en el pool."""
    pass


class Pool:
    _instance = None
    _factory = None
    _factory_type = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Pool, cls).__new__(cls)
        return cls._instance
        
    def get_factory(self, factory_class):
        if self._factory is not None:
            if self._factory_type != factory_class:
                raise FactoryYaExiste(f"Ya exuiste la fabrica {self._factory_type.__name__} elimina la anterior para rear una nueva")
            return self._factory
        
        self._factory = factory_class()
        self._factory_type = factory_class
        return self._factory
    
    def remove_factory(self, factory_class=None):
        """
        Elimina la fábrica del pool solo si coincide con el tipo especificado.
        Si no se especifica factory_class, elimina cualquier fábrica.
        """
        if factory_class is None:
            # Sin validación - eliminar cualquier fábrica
            self._factory = None
            self._factory_type = None
            return True
            
        if self._factory is None:
            return False  # No hay fábrica que eliminar
            
        if self._factory_type == factory_class:
            # Solo eliminar si es del mismo tipo
            self._factory = None
            self._factory_type = None
            return True
        else:
            return False  # No se puede eliminar una fábrica de diferente tipo
    
    def get_current_factory_info(self):
        """Obtiene información sobre la fábrica actual en el pool"""
        return {
            "has_factory": self._factory is not None,
            "factory_type": self._factory_type.__name__ if self._factory_type else None,
            "factory_instance": str(self._factory) if self._factory else None
        }
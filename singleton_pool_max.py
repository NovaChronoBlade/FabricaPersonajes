from abc import ABC, abstractmethod, ABCMeta
from typing import Dict, List, Type, Any, Optional
import threading
from queue import Queue


class FactoryYaExiste(Exception):
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
    
    def remove_factory(self):
        self._factory = None
        self._factory_type = None




# class SingletonABCMeta(ABCMeta):
#     """
#     Metaclass que combina Singleton + ABC para evitar conflictos.
#     Permite usar abstractmethod junto con singleton.
#     """
#     _instances: Dict[Type, Any] = {}
#     _lock: threading.Lock = threading.Lock()

#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             with cls._lock:
#                 if cls not in cls._instances:
#                     cls._instances[cls] = super().__call__(*args, **kwargs)
#         return cls._instances[cls]


# class FactoryPoolSingleton(metaclass=SingletonABCMeta):
#     """
#     Clase base que combina Singleton + Object Pool para las fábricas.
#     Cada fábrica será un singleton que mantiene pools de objetos.
#     """
    
#     def __init__(self, max_size: int = 10):
#         self._max_size = max_size
#         self._lock = threading.Lock()
#         # Pools separados para cada tipo de objeto
#         self._cuerpo_pool: Queue = Queue(maxsize=max_size)
#         self._montura_pool: Queue = Queue(maxsize=max_size)
#         self._armadura_pool: Queue = Queue(maxsize=max_size)
#         self._arma_pool: Queue = Queue(maxsize=max_size)
        
#         # Contadores para cada tipo
#         self._created_cuerpos = 0
#         self._created_monturas = 0
#         self._created_armaduras = 0
#         self._created_armas = 0
    
#     @abstractmethod
#     def _create_new_cuerpo(self):
#         """Crea una nueva instancia de cuerpo."""
#         pass
    
#     @abstractmethod
#     def _create_new_montura(self):
#         """Crea una nueva instancia de montura."""
#         pass
    
#     @abstractmethod
#     def _create_new_armadura(self):
#         """Crea una nueva instancia de armadura."""
#         pass
    
#     @abstractmethod
#     def _create_new_arma(self):
#         """Crea una nueva instancia de arma."""
#         pass
    
#     def _reset_cuerpo(self, obj) -> None:
#         """Reinicia el estado del cuerpo. Puede ser sobrescrito."""
#         pass
    
#     def _reset_montura(self, obj) -> None:
#         """Reinicia el estado de la montura. Puede ser sobrescrito."""
#         pass
    
#     def _reset_armadura(self, obj) -> None:
#         """Reinicia el estado de la armadura. Puede ser sobrescrito."""
#         pass
    
#     def _reset_arma(self, obj) -> None:
#         """Reinicia el estado del arma. Puede ser sobrescrito."""
#         pass
    
#     def get_cuerpo(self, timeout=10):
#         """Obtiene un cuerpo del pool o crea uno nuevo."""
#         try:
#             return self._cuerpo_pool.get_nowait()
#         except:
#             with self._lock:
#                 if self._created_cuerpos < self._max_size:
#                     obj = self._create_new_cuerpo()
#                     self._created_cuerpos += 1
#                     return obj
#                 else:
#                     # En lugar de bloquear indefinidamente, usar timeout
#                     try:
#                         return self._cuerpo_pool.get(timeout=timeout)
#                     except:
#                         raise RuntimeError(f"Pool exhausted: No hay objetos disponibles después de {timeout}s. "
#                                          f"Creados: {self._created_cuerpos}/{self._max_size}, "
#                                          f"Pool size: {self._cuerpo_pool.qsize()}")
    
#     def get_montura(self, timeout=10):
#         """Obtiene una montura del pool o crea una nueva."""
#         try:
#             return self._montura_pool.get_nowait()
#         except:
#             with self._lock:
#                 if self._created_monturas < self._max_size:
#                     obj = self._create_new_montura()
#                     self._created_monturas += 1
#                     return obj
#                 else:
#                     try:
#                         return self._montura_pool.get(timeout=timeout)
#                     except:
#                         raise RuntimeError(f"Pool exhausted: No hay monturas disponibles después de {timeout}s. "
#                                          f"Creados: {self._created_monturas}/{self._max_size}, "
#                                          f"Pool size: {self._montura_pool.qsize()}")
    
#     def get_armadura(self, timeout=10):
#         """Obtiene una armadura del pool o crea una nueva."""
#         try:
#             return self._armadura_pool.get_nowait()
#         except:
#             with self._lock:
#                 if self._created_armaduras < self._max_size:
#                     obj = self._create_new_armadura()
#                     self._created_armaduras += 1
#                     return obj
#                 else:
#                     try:
#                         return self._armadura_pool.get(timeout=timeout)
#                     except:
#                         raise RuntimeError(f"Pool exhausted: No hay armaduras disponibles después de {timeout}s. "
#                                          f"Creados: {self._created_armaduras}/{self._max_size}, "
#                                          f"Pool size: {self._armadura_pool.qsize()}")
    
#     def get_arma(self, timeout=10):
#         """Obtiene un arma del pool o crea una nueva."""
#         try:
#             return self._arma_pool.get_nowait()
#         except:
#             with self._lock:
#                 if self._created_armas < self._max_size:
#                     obj = self._create_new_arma()
#                     self._created_armas += 1
#                     return obj
#                 else:
#                     try:
#                         return self._arma_pool.get(timeout=timeout)
#                     except:
#                         raise RuntimeError(f"Pool exhausted: No hay armas disponibles después de {timeout}s. "
#                                          f"Creados: {self._created_armas}/{self._max_size}, "
#                                          f"Pool size: {self._arma_pool.qsize()}")
    
#     def return_cuerpo(self, obj) -> None:
#         """Devuelve un cuerpo al pool."""
#         if obj is not None:
#             self._reset_cuerpo(obj)
#             try:
#                 self._cuerpo_pool.put_nowait(obj)
#             except:
#                 pass
    
#     def return_montura(self, obj) -> None:
#         """Devuelve una montura al pool."""
#         if obj is not None:
#             self._reset_montura(obj)
#             try:
#                 self._montura_pool.put_nowait(obj)
#             except:
#                 pass
    
#     def return_armadura(self, obj) -> None:
#         """Devuelve una armadura al pool."""
#         if obj is not None:
#             self._reset_armadura(obj)
#             try:
#                 self._armadura_pool.put_nowait(obj)
#             except:
#                 pass
    
#     def return_arma(self, obj) -> None:
#         """Devuelve un arma al pool."""
#         if obj is not None:
#             self._reset_arma(obj)
#             try:
#                 self._arma_pool.put_nowait(obj)
#             except:
#                 pass
    
#     def get_pool_stats(self) -> Dict[str, int]:
#         """Retorna estadísticas de los pools."""
#         return {
#             'cuerpo_pool_size': self._cuerpo_pool.qsize(),
#             'montura_pool_size': self._montura_pool.qsize(),
#             'armadura_pool_size': self._armadura_pool.qsize(),
#             'arma_pool_size': self._arma_pool.qsize(),
#             'created_cuerpos': self._created_cuerpos,
#             'created_monturas': self._created_monturas,
#             'created_armaduras': self._created_armaduras,
#             'created_armas': self._created_armas,
#         }


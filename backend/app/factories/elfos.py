from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager
from ..patterns.singleton_pool import FactoryPoolSingleton


class CuerpoElfo(ICuerpo):

    def obtener_informacion(self) -> dict:
        info = {
            "cuerpo_img": image_manager.get_web_path("characters", "elfo/elfo_cuerpo.png"),
            "especie": "Elfo",
            "altura": "1.80m",
            "peso": "70kg",
            "habilidades": ["Visión nocturna", "Agilidad", "Magia"]
        }
        return info

    def analizar(self) -> None:
        print("Analizando cuerpo elfo...")


class MonturaElfo(IMontura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "elfo_montura.png"),
            "tipo": "Caballo élfico",
            "velocidad": "Muy rápida",
            "habilidades": ["Vuelo corto", "Salto alto"]
        }
    
    def montar(self) -> None:
        print("Montando caballo elfo.")

    def bajarse(self) -> None:
        print("Bajándose del caballo elfo.")


class ArmaduraElfo(IArmadura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "elfo_armadura.png"),
            "tipo": "Armadura élfica",
            "material": "Mithril",
            "defensa": "Alta",
            "peso": "Ligera"
        }
    
    def equipar(self) -> None:
        print("Equipando armadura elfo.")

    def arrojar(self) -> None:
        print("Arrojando armadura elfo.")


class ArmaElfo(IArma):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "elfo_arma.png"),
            "tipo": "Arco élfico",
            "material": "Madera sagrada",
            "daño": "Alto",
            "alcance": "Largo"
        }
    
    def atacar(self) -> None:
        print("Elfo ataca con Arco.")

    def parry(self) -> None:
        print("Elfo hace parry con escudo elfico.")


class FabricarElfos(FactoryPoolSingleton, FactoryAbstract):
    """
    Fábrica Singleton con Pool de Objetos para crear personajes Elfos.
    Mantiene pools separados para cada tipo de objeto y reutiliza instancias.
    """
    
    def __init__(self, max_size: int = 10):
        super().__init__(max_size)
    
    # Implementación de métodos abstractos de FactoryPoolSingleton
    def _create_new_cuerpo(self):
        return CuerpoElfo()
    
    def _create_new_montura(self):
        return MonturaElfo()
    
    def _create_new_armadura(self):
        return ArmaduraElfo()
    
    def _create_new_arma(self):
        return ArmaElfo()
    
    # Implementación de métodos de FactoryAbstract usando el pool
    def crear_cuerpo(self) -> ICuerpo:
        return self.get_cuerpo()

    def crear_montura(self) -> IMontura:
        return self.get_montura()

    def crear_armadura(self) -> IArmadura:
        return self.get_armadura()

    def crear_arma(self) -> IArma:
        return self.get_arma()
    
    # Métodos adicionales para devolver objetos al pool
    def devolver_cuerpo(self, cuerpo: ICuerpo) -> None:
        """Devuelve un cuerpo al pool para su reutilización."""
        self.return_cuerpo(cuerpo)
    
    def devolver_montura(self, montura: IMontura) -> None:
        """Devuelve una montura al pool para su reutilización."""
        self.return_montura(montura)
    
    def devolver_armadura(self, armadura: IArmadura) -> None:
        """Devuelve una armadura al pool para su reutilización."""
        self.return_armadura(armadura)
    
    def devolver_arma(self, arma: IArma) -> None:
        """Devuelve un arma al pool para su reutilización."""
        self.return_arma(arma)

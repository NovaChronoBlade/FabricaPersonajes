from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager


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


class FabricarElfos(FactoryAbstract):
    """
    Fábrica Singleton con Pool de Objetos para crear personajes Elfos.
    Mantiene pools separados para cada tipo de objeto y reutiliza instancias.
    """
    
    def __init__(self, max_size: int = 10):
        super().__init__()
    
    # Implementación de métodos abstractos de FactoryAbstract
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoElfo()
    
    def crear_montura(self) -> IMontura:
        return MonturaElfo()
    
    def crear_armadura(self) -> IArmadura:
        return ArmaduraElfo()
    
    def crear_arma(self) -> IArma:
        return ArmaElfo()
    
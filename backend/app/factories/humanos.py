from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager


class CuerpoHumano(ICuerpo):
    def obtener_informacion(self) -> dict:
        info = {
            "cuerpo_img": image_manager.get_web_path("characters", "humano/humano_cuerpo.png"),
            "especie": "Humano",
            "altura": "1.75m",
            "peso": "75kg",
            "habilidades": ["Adaptabilidad", "Versatilidad", "Liderazgo"]
        }
        return info

    def analizar(self) -> None:
        print("Analizando cuerpo humano...")


class MonturaHumano(IMontura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "humano/humano_montura.png"),
            "tipo": "Caballo de guerra",
            "velocidad": "Rápida",
            "habilidades": ["Velocidad", "Salto", "Resistencia"]
        }

    def montar(self) -> None:
        print("Montando caballo humano.")

    def bajarse(self) -> None:
        print("Bajándose del caballo humano.")


class ArmaduraHumano(IArmadura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "humano/humano_armadura.png"),
            "tipo": "Armadura de cota de malla",
            "material": "Acero templado",
            "defensa": "Media-Alta",
            "peso": "Media"
        }

    def equipar(self) -> None:
        print("Equipando armadura humana.")

    def arrojar(self) -> None:
        print("Arrojando armadura humana.")


class ArmaHumano(IArma):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "humano/humano_arma.png"),
            "tipo": "Espada larga",
            "material": "Acero forjado",
            "daño": "Alto",
            "alcance": "Medio"
        }

    def atacar(self) -> None:
        print("Humano ataca con espada.")

    def parry(self) -> None:
        print("Humano hace parry con escudo.")


class FabricarHumanos(FactoryAbstract):
    """
    Fábrica Singleton con Pool de Objetos para crear personajes Humanos.
    Mantiene pools separados para cada tipo de objeto y reutiliza instancias.
    """    
    # Implementación de métodos abstractos de FactoryAbstract
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoHumano()
    
    def crear_montura(self) -> IMontura:
        return MonturaHumano()
    
    def crear_armadura(self) -> IArmadura:
        return ArmaduraHumano()
    
    def crear_arma(self) -> IArma:
        return ArmaHumano()
    
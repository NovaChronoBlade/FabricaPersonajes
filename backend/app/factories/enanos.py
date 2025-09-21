from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager


class CuerpoEnano(ICuerpo):
    def obtener_informacion(self) -> dict:
        info = {
            "cuerpo_img": image_manager.get_web_path("characters", "enano/enano_cuerpo.png"),
            "especie": "Enano",
            "altura": "1.40m",
            "peso": "80kg",
            "habilidades": ["Resistencia", "Fuerza", "Artesanía"]
        }
        return info

    def analizar(self) -> None:
        print("Analizando cuerpo enano...")


class MonturaEnano(IMontura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "enano_montura.png"),
            "tipo": "Jabalí de guerra",
            "velocidad": "Media",
            "habilidades": ["Carga", "Resistencia", "Terreno difícil"]
        }

    def montar(self) -> None:
        print("Montando jabalí enano.")

    def bajarse(self) -> None:
        print("Bajándose del jabalí enano.")


class ArmaduraEnano(IArmadura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "enano_armadura.png"),
            "tipo": "Armadura de placas",
            "material": "Acero forjado",
            "defensa": "Muy alta",
            "peso": "Pesada"
        }

    def equipar(self) -> None:
        print("Equipando armadura enana.")

    def arrojar(self) -> None:
        print("Arrojando armadura enana.")


class ArmaEnano(IArma):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "enano_arma.png"),
            "tipo": "Martillo de guerra",
            "material": "Hierro macizo",
            "daño": "Muy alto",
            "alcance": "Corto"
        }

    def atacar(self) -> None:
        print("Enano ataca con martillo.")

    def parry(self) -> None:
        print("Enano bloquea con escudo.")


class FabricarEnanos(FactoryAbstract):
    """
    Fábrica Singleton con Pool de Objetos para crear personajes Enanos.
    Mantiene pools separados para cada tipo de objeto y reutiliza instancias.
    """

    # Implementación de métodos abstractos de FactoryAbstract
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoEnano()
    
    def crear_montura(self) -> IMontura:
        return MonturaEnano()

    def crear_armadura(self) -> IArmadura:
        return ArmaduraEnano()

    def crear_arma(self) -> IArma:
        return ArmaEnano()
    
    
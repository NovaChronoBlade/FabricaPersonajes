from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager


class CuerpoOrco(ICuerpo):
    def obtener_informacion(self) -> dict:
        info = {
            "cuerpo_img": image_manager.get_web_path("characters", "orco/orco_cuerpo.png"),
            "avatar_img": image_manager.get_web_path("avatars", "orco_avatar.png"),
            "especie": "Orco",
            "altura": "1.90m",
            "peso": "95kg",
            "habilidades": ["Fuerza bruta", "Intimidación", "Resistencia al dolor"]
        }
        return info

    def analizar(self) -> None:
        print("Analizando cuerpo orco...")


class MonturaOrco(IMontura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "orco/orco_montura.png"),
            "tipo": "Warg",
            "velocidad": "Muy rápida",
            "habilidades": ["Ferocidad", "Rastreo", "Ataque en manada"]
        }

    def montar(self) -> None:
        print("Montando jabalí orco.")

    def bajarse(self) -> None:
        print("Bajándose del jabalí orco.")


class ArmaduraOrco(IArmadura):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "orco/orco_armadura.png"),
            "tipo": "Armadura de cuero tachonado",
            "material": "Cuero y metal",
            "defensa": "Media",
            "peso": "Media-Ligera"
        }

    def equipar(self) -> None:
        print("Equipando armadura orca.")

    def arrojar(self) -> None:
        print("Arrojando armadura orca.")


class ArmaOrco(IArma):
    def obtener_informacion(self) -> dict:
        return {
            "imagen": image_manager.get_web_path("characters", "orco/orco_arma.png"),
            "tipo": "Hacha de guerra",
            "material": "Hierro crudo",
            "daño": "Muy alto",
            "alcance": "Medio-Corto"
        }

    def atacar(self) -> None:
        print("Orco ataca con Hacha.")

    def parry(self) -> None:
        print("Orco hace parry con escudo orco.")


class FabricarOrcos(FactoryAbstract):
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoOrco()

    def crear_montura(self) -> IMontura:
        return MonturaOrco()

    def crear_armadura(self) -> IArmadura:
        return ArmaduraOrco()

    def crear_arma(self) -> IArma:
        return ArmaOrco()

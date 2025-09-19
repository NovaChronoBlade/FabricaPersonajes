from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager
from ..patterns.singleton_pool import FactoryPoolSingleton


class CuerpoOrco(ICuerpo):
    def obtener_informacion(self) -> dict:
        info = {
            "cuerpo_img": image_manager.get_web_path("characters", "orco/orco_cuerpo.png"),
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


class FabricarOrcos(FactoryPoolSingleton, FactoryAbstract):
    """
    Fábrica Singleton con Pool de Objetos para crear personajes Orcos.
    Mantiene pools separados para cada tipo de objeto y reutiliza instancias.
    """
    
    def __init__(self, max_size: int = 10):
        super().__init__(max_size)
    
    # Implementación de métodos abstractos de FactoryPoolSingleton
    def _create_new_cuerpo(self):
        return CuerpoOrco()
    
    def _create_new_montura(self):
        return MonturaOrco()
    
    def _create_new_armadura(self):
        return ArmaduraOrco()
    
    def _create_new_arma(self):
        return ArmaOrco()
    
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

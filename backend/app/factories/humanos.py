from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager
from ..patterns.singleton_pool import FactoryPoolSingleton


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
            "imagen": image_manager.get_web_path("characters", "humano_montura.png"),
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
            "imagen": image_manager.get_web_path("characters", "humano_armadura.png"),
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
            "imagen": image_manager.get_web_path("characters", "humano_arma.png"),
            "tipo": "Espada larga",
            "material": "Acero forjado",
            "daño": "Alto",
            "alcance": "Medio"
        }

    def atacar(self) -> None:
        print("Humano ataca con espada.")

    def parry(self) -> None:
        print("Humano hace parry con escudo.")


class FabricarHumanos(FactoryPoolSingleton, FactoryAbstract):
    """
    Fábrica Singleton con Pool de Objetos para crear personajes Humanos.
    Mantiene pools separados para cada tipo de objeto y reutiliza instancias.
    """
    
    def __init__(self, max_size: int = 10):
        super().__init__(max_size)
    
    # Implementación de métodos abstractos de FactoryPoolSingleton
    def _create_new_cuerpo(self):
        return CuerpoHumano()
    
    def _create_new_montura(self):
        return MonturaHumano()
    
    def _create_new_armadura(self):
        return ArmaduraHumano()
    
    def _create_new_arma(self):
        return ArmaHumano()
    
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

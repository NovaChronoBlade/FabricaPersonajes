from ..interfaces.interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura
from ..utils.image_manager import image_manager
from ..patterns.singleton_pool import FactoryPoolSingleton


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


class FabricarEnanos(FactoryPoolSingleton, FactoryAbstract):
    """
    Fábrica Singleton con Pool de Objetos para crear personajes Enanos.
    Mantiene pools separados para cada tipo de objeto y reutiliza instancias.
    """
    
    def __init__(self, max_size: int = 10):
        super().__init__(max_size)
    
    # Implementación de métodos abstractos de FactoryPoolSingleton
    def _create_new_cuerpo(self):
        return CuerpoEnano()
    
    def _create_new_montura(self):
        return MonturaEnano()
    
    def _create_new_armadura(self):
        return ArmaduraEnano()
    
    def _create_new_arma(self):
        return ArmaEnano()
    
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

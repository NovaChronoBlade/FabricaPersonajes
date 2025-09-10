# Implementaciones concretas de productos (Humanos)
from interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura


class CuerpoHumano(ICuerpo):
    def analizar(self) -> None:
        print("Analizando cuerpo humano...")


class MonturaHumano(IMontura):
    def montar(self) -> None:
        print("Montando caballo humano.")

    def bajarse(self) -> None:
        print("Bajándose del caballo humano.")


class ArmaduraHumano(IArmadura):
    def equipar(self) -> None:
        print("Equipando armadura humana.")

    def arrojar(self) -> None:
        print("Arrojando armadura humana.")


class ArmaHumano(IArma):
    def atacar(self) -> None:
        print("Humano ataca con espada.")

    def parry(self) -> None:
        print("Humano hace parry con escudo.")


# Fábricas concretas
class FabricarHumanos(FactoryAbstract):
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoHumano()

    def crear_montura(self) -> IMontura:
        return MonturaHumano()

    def crear_armadura(self) -> IArmadura:
        return ArmaduraHumano()

    def crear_arma(self) -> IArma:
        return ArmaHumano()

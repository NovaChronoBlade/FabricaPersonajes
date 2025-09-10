# Implementaciones concretas de productos (Elfos)
from interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura


class CuerpoElfo(ICuerpo):
    def analizar(self) -> None:
        print("Analizando cuerpo elfo...")


class MonturaElfo(IMontura):
    def montar(self) -> None:
        print("Montando caballo elfo.")

    def bajarse(self) -> None:
        print("Bajándose del caballo elfo.")


class ArmaduraElfo(IArmadura):
    def equipar(self) -> None:
        print("Equipando armadura elfo.")

    def arrojar(self) -> None:
        print("Arrojando armadura elfo.")


class ArmaElfo(IArma):
    def atacar(self) -> None:
        print("Elfo ataca con Arco.")

    def parry(self) -> None:
        print("Elfo hace parry con escudo elfico.")


# Fábricas concretas
class FabricarElfos(FactoryAbstract):
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoElfo()

    def crear_montura(self) -> IMontura:
        return MonturaElfo()

    def crear_armadura(self) -> IArmadura:
        return ArmaduraElfo()

    def crear_arma(self) -> IArma:
        return ArmaElfo()

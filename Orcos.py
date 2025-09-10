# Implementaciones concretas de productos (Orcos)
from interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura


class CuerpoOrco(ICuerpo):
    def analizar(self) -> None:
        print("Analizando cuerpo orco...")


class MonturaOrco(IMontura):
    def montar(self) -> None:
        print("Montando jabalí orco.")

    def bajarse(self) -> None:
        print("Bajándose del jabalí orco.")


class ArmaduraOrco(IArmadura):
    def equipar(self) -> None:
        print("Equipando armadura orca.")

    def arrojar(self) -> None:
        print("Arrojando armadura orca.")


class ArmaOrco(IArma):
    def atacar(self) -> None:
        print("Orco ataca con Hacha.")

    def parry(self) -> None:
        print("Orco hace parry con escudo orco.")


# Fábricas concretas
class FabricarOrcos(FactoryAbstract):
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoOrco()

    def crear_montura(self) -> IMontura:
        return MonturaOrco()

    def crear_armadura(self) -> IArmadura:
        return ArmaduraOrco()

    def crear_arma(self) -> IArma:
        return ArmaOrco()

from interfaces import FactoryAbstract, IArma, IArmadura, ICuerpo, IMontura


# Implementaciones concretas de productos (Enanos)
class CuerpoEnano(ICuerpo):
    def analizar(self) -> None:
        print("Analizando cuerpo enano...")


class MonturaEnano(IMontura):
    def montar(self) -> None:
        print("Montando jabalí enano.")

    def bajarse(self) -> None:
        print("Bajándose del jabalí enano.")


class ArmaduraEnano(IArmadura):
    def equipar(self) -> None:
        print("Equipando armadura enana.")

    def arrojar(self) -> None:
        print("Arrojando armadura enana.")


class ArmaEnano(IArma):
    def atacar(self) -> None:
        print("Enano ataca con martillo.")

    def parry(self) -> None:
        print("Enano bloquea con escudo.")


class FabricarEnanos(FactoryAbstract):
    def crear_cuerpo(self) -> ICuerpo:
        return CuerpoEnano()

    def crear_montura(self) -> IMontura:
        return MonturaEnano()

    def crear_armadura(self) -> IArmadura:
        return ArmaduraEnano()

    def crear_arma(self) -> IArma:
        return ArmaEnano()

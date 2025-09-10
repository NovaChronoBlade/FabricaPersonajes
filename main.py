# Cliente
from Elfos import FabricarElfos
from Enanos import FabricarEnanos
from Humanos import FabricarHumanos
from Orcos import FabricarOrcos
from interfaces import FactoryAbstract


class Cliente:
    def __init__(self, fabrica: FactoryAbstract):
        self.fabrica = fabrica

    def solicitar(self):
        cuerpo = self.fabrica.crear_cuerpo()
        montura = self.fabrica.crear_montura()
        armadura = self.fabrica.crear_armadura()
        arma = self.fabrica.crear_arma()

        cuerpo.analizar()
        montura.montar()
        armadura.equipar()
        arma.atacar()


if __name__ == "__main__":
    print("=== Humanos ===")
    cliente_humano = Cliente(FabricarHumanos())
    cliente_humano.solicitar()

    print("\n=== Enanos ===")
    cliente_enano = Cliente(FabricarEnanos())
    cliente_enano.solicitar()

    print("\n=== Orcos ===")
    cliente_orco = Cliente(FabricarOrcos())
    cliente_orco.solicitar()
    print("\n=== Elfos ===")
    cliente_elfo = Cliente(FabricarElfos())
    cliente_elfo.solicitar()

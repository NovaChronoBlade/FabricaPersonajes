from abc import ABC, abstractmethod


# Interfaces de productos
class ICuerpo(ABC):
    @abstractmethod
    def analizar(self) -> None:
        pass


class IMontura(ABC):
    @abstractmethod
    def montar(self) -> None:
        pass

    @abstractmethod
    def bajarse(self) -> None:
        pass


class IArmadura(ABC):
    @abstractmethod
    def equipar(self) -> None:
        pass

    @abstractmethod
    def arrojar(self) -> None:
        pass


class IArma(ABC):
    @abstractmethod
    def atacar(self) -> None:
        pass


# Interfaz Abstract Factory
class FactoryAbstract(ABC):
    @abstractmethod
    def crear_cuerpo(self) -> ICuerpo: ...
    @abstractmethod
    def crear_montura(self) -> IMontura: ...
    @abstractmethod
    def crear_armadura(self) -> IArmadura: ...
    @abstractmethod
    def crear_arma(self) -> IArma: ...

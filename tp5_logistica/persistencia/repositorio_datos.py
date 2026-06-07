from abc import ABC, abstractmethod


class RepositorioDatos(ABC):
    @abstractmethod
    def guardar(self, datos):
        pass

    @abstractmethod
    def cargar(self):
        pass
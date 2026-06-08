from abc import ABC, abstractmethod

class IntervencionMantenimiento(ABC):
    def __init__(self, fecha, kilometraje, descripcion, costo_base):
        self._fecha = fecha
        self._kilometraje = kilometraje
        self._descripcion = descripcion
        self._costo_base = costo_base

    @property
    def fecha(self):
        return self._fecha

    @property
    def kilometraje(self):
        return self._kilometraje

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def costo_base(self):
        return self._costo_base

    @abstractmethod
    def obtener_tipo(self):
        pass

    @abstractmethod
    def calcular_costo_estimado(self):
        pass

    @abstractmethod
    def generar_reporte(self):
        pass

    def to_dict(self):
        return {
            "tipo_clase": self.__class__.__name__,
            "fecha": self._fecha,
            "kilometraje": self._kilometraje,
            "descripcion": self._descripcion,
            "costo_base": self._costo_base,
        }
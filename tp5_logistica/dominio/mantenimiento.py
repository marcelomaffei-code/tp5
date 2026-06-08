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

def mantenimiento_from_dict(data):
    """Factory para reconstruir intervenciones desde dict (imports relativos)."""
    tipo = data.get("tipo_clase")
    if tipo == "IntervencionPreventiva":
        from .intervencion_preventiva import IntervencionPreventiva
        return IntervencionPreventiva(
            fecha=data.get("fecha"),
            kilometraje=data.get("kilometraje"),
            descripcion=data.get("descripcion"),
            costo_base=data.get("costo_base"),
            revision_programada=data.get("revision_programada"),
        )

    if tipo == "IntervencionCorrectiva":
        from .intervencion_correctiva import IntervencionCorrectiva
        return IntervencionCorrectiva(
            fecha=data.get("fecha"),
            kilometraje=data.get("kilometraje"),
            descripcion=data.get("descripcion"),
            costo_base=data.get("costo_base"),
            gravedad_falla=data.get("gravedad_falla"),
        )

    raise ValueError(f"Tipo de mantenimiento inválido: {tipo}")
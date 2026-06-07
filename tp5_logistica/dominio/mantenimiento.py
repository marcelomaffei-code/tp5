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


class IntervencionPreventiva(IntervencionMantenimiento):
    def __init__(self, fecha, kilometraje, descripcion, costo_base, revision_programada):
        super().__init__(fecha, kilometraje, descripcion, costo_base)
        self._revision_programada = revision_programada

    @property
    def revision_programada(self):
        return self._revision_programada

    def obtener_tipo(self):
        return "preventiva"

    def calcular_costo_estimado(self):
        recargo_programacion = 0

        if self._revision_programada:
            recargo_programacion = self._costo_base * 0.10

        return self._costo_base + recargo_programacion

    def generar_reporte(self):
        return (
            f"Mantenimiento preventivo - Fecha: {self._fecha} - "
            f"Km: {self._kilometraje} - "
            f"Descripción: {self._descripcion} - "
            f"Costo estimado: {self.calcular_costo_estimado()}"
        )

    def to_dict(self):
        data = super().to_dict()
        data["revision_programada"] = self._revision_programada
        return data


class IntervencionCorrectiva(IntervencionMantenimiento):
    def __init__(self, fecha, kilometraje, descripcion, costo_base, gravedad_falla):
        super().__init__(fecha, kilometraje, descripcion, costo_base)
        self._gravedad_falla = gravedad_falla

    @property
    def gravedad_falla(self):
        return self._gravedad_falla

    def obtener_tipo(self):
        return "correctiva"

    def calcular_costo_estimado(self):
        multiplicador = 1.0

        if self._gravedad_falla.lower() == "media":
            multiplicador = 1.25
        elif self._gravedad_falla.lower() == "alta":
            multiplicador = 1.50

        return self._costo_base * multiplicador

    def generar_reporte(self):
        return (
            f"Mantenimiento correctivo - Fecha: {self._fecha} - "
            f"Km: {self._kilometraje} - "
            f"Descripción: {self._descripcion} - "
            f"Gravedad: {self._gravedad_falla} - "
            f"Costo estimado: {self.calcular_costo_estimado()}"
        )

    def to_dict(self):
        data = super().to_dict()
        data["gravedad_falla"] = self._gravedad_falla
        return data


def mantenimiento_from_dict(data):
    tipo_clase = data["tipo_clase"]

    if tipo_clase == "IntervencionPreventiva":
        return IntervencionPreventiva(
            fecha=data["fecha"],
            kilometraje=data["kilometraje"],
            descripcion=data["descripcion"],
            costo_base=data["costo_base"],
            revision_programada=data["revision_programada"],
        )

    if tipo_clase == "IntervencionCorrectiva":
        return IntervencionCorrectiva(
            fecha=data["fecha"],
            kilometraje=data["kilometraje"],
            descripcion=data["descripcion"],
            costo_base=data["costo_base"],
            gravedad_falla=data["gravedad_falla"],
        )

    raise ValueError("Tipo de mantenimiento inválido.")
from datetime import datetime
from dominio.enums import EstadoEnvio

class EventoHistorial:
    def __init__(self, descripcion, estado_anterior=None, estado_nuevo=None, fecha_hora=None):
        if estado_anterior is not None and not isinstance(estado_anterior, EstadoEnvio):
            raise ValueError("Estado anterior inválido.")

        if estado_nuevo is not None and not isinstance(estado_nuevo, EstadoEnvio):
            raise ValueError("Estado nuevo inválido.")

        self._fecha_hora = fecha_hora if fecha_hora is not None else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._descripcion = descripcion
        self._estado_anterior = estado_anterior
        self._estado_nuevo = estado_nuevo

    @property
    def fecha_hora(self):
        return self._fecha_hora

    @property
    def descripcion(self):
        return self._descripcion

    @property
    def estado_anterior(self):
        return self._estado_anterior

    @property
    def estado_nuevo(self):
        return self._estado_nuevo

    def generar_descripcion(self):
        estado_anterior = "sin estado anterior"
        estado_nuevo = "sin estado nuevo"

        if self._estado_anterior is not None:
            estado_anterior = self._estado_anterior.value

        if self._estado_nuevo is not None:
            estado_nuevo = self._estado_nuevo.value

        return (
            f"[{self._fecha_hora}] {self._descripcion} "
            f"({estado_anterior} -> {estado_nuevo})"
        )

    def obtener_resumen(self):
        return self.generar_descripcion()

    def to_dict(self):
        return {
            "fecha_hora": self._fecha_hora,
            "descripcion": self._descripcion,
            "estado_anterior": (
                self._estado_anterior.value
                if self._estado_anterior is not None
                else None
            ),
            "estado_nuevo": (
                self._estado_nuevo.value
                if self._estado_nuevo is not None
                else None
            ),
        }

    @staticmethod
    def from_dict(data):
        estado_anterior = None
        estado_nuevo = None

        if data["estado_anterior"] is not None:
            estado_anterior = EstadoEnvio(data["estado_anterior"])

        if data["estado_nuevo"] is not None:
            estado_nuevo = EstadoEnvio(data["estado_nuevo"])

        return EventoHistorial(
            descripcion=data["descripcion"],
            estado_anterior=estado_anterior,
            estado_nuevo=estado_nuevo,
            fecha_hora=data["fecha_hora"],
        )
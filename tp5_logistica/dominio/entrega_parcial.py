from dominio.enums import EstadoEntregaParcial


class EntregaParcial:
    def __init__(self, punto_entrega, fecha_entrega, detalle_carga):
        self._punto_entrega = punto_entrega
        self._fecha_entrega = fecha_entrega
        self._detalle_carga = detalle_carga
        self._estado = EstadoEntregaParcial.PENDIENTE

    @property
    def punto_entrega(self):
        return self._punto_entrega

    @property
    def fecha_entrega(self):
        return self._fecha_entrega

    @property
    def detalle_carga(self):
        return self._detalle_carga

    @property
    def estado(self):
        return self._estado

    def marcar_entregada(self):
        self._estado = EstadoEntregaParcial.ENTREGADA

    def esta_entregada(self):
        return self._estado == EstadoEntregaParcial.ENTREGADA

    def generar_resumen(self):
        return (
            f"Entrega parcial en {self._punto_entrega} - "
            f"Fecha: {self._fecha_entrega} - "
            f"Estado: {self._estado.value} - "
            f"Detalle: {self._detalle_carga}"
        )

    def to_dict(self):
        return {
            "punto_entrega": self._punto_entrega,
            "fecha_entrega": self._fecha_entrega,
            "estado": self._estado.value,
            "detalle_carga": self._detalle_carga,
        }

    @staticmethod
    def from_dict(data):
        entrega = EntregaParcial(
            data["punto_entrega"],
            data["fecha_entrega"],
            data["detalle_carga"]
        )

        if data["estado"] == EstadoEntregaParcial.ENTREGADA.value:
            entrega.marcar_entregada()

        return entrega
from dominio.enums import EstadoEnvio, EstadoVehiculo
from dominio.evento_historial import EventoHistorial

class Envio:
    def __init__(
        self,
        numero_seguimiento,
        origen,
        destino,
        fecha_salida_programada,
        fecha_llegada_estimada,
        vehiculo,
        tipo_carga,
    ):
        self._numero_seguimiento = numero_seguimiento
        self._origen = origen
        self._destino = destino
        self._fecha_salida_programada = fecha_salida_programada
        self._fecha_llegada_estimada = fecha_llegada_estimada
        self._vehiculo = vehiculo
        self._tipo_carga = tipo_carga
        self._estado = EstadoEnvio.PENDIENTE
        self._entregas_parciales = []
        self._historial = []

        self.agregar_evento_historial(
            EventoHistorial(
                "Envío creado",
                None,
                EstadoEnvio.PENDIENTE
            )
        )

    @property
    def numero_seguimiento(self):
        return self._numero_seguimiento

    @property
    def origen(self):
        return self._origen

    @property
    def destino(self):
        return self._destino

    @property
    def fecha_salida_programada(self):
        return self._fecha_salida_programada

    @property
    def fecha_llegada_estimada(self):
        return self._fecha_llegada_estimada

    @property
    def vehiculo(self):
        return self._vehiculo

    @property
    def tipo_carga(self):
        return self._tipo_carga

    @property
    def estado(self):
        return self._estado

    @property
    def entregas_parciales(self):
        return self._entregas_parciales

    @property
    def historial(self):
        return self._historial

    def validar_transicion(self, nuevo_estado):
        if not isinstance(nuevo_estado, EstadoEnvio):
            raise ValueError("Estado de envío inválido.")

        transicion_valida = False

        if self._estado == EstadoEnvio.PENDIENTE:
            transicion_valida = nuevo_estado in [
                EstadoEnvio.EN_TRANSITO,
                EstadoEnvio.CANCELADO
            ]

        elif self._estado == EstadoEnvio.EN_TRANSITO:
            transicion_valida = nuevo_estado in [
                EstadoEnvio.ENTREGADO,
                EstadoEnvio.CANCELADO
            ]

        elif self._estado == EstadoEnvio.ENTREGADO:
            transicion_valida = False

        elif self._estado == EstadoEnvio.CANCELADO:
            transicion_valida = False

        return transicion_valida

    def iniciar_transito(self):
        nuevo_estado = EstadoEnvio.EN_TRANSITO

        if not self.validar_transicion(nuevo_estado):
            raise ValueError("No se puede iniciar el envío desde el estado actual.")

        estado_anterior = self._estado
        self._estado = nuevo_estado

        self._vehiculo.cambiar_estado(EstadoVehiculo.EN_RUTA)

        self.agregar_evento_historial(
            EventoHistorial(
                "Envío iniciado",
                estado_anterior,
                nuevo_estado
            )
        )

    def registrar_entrega_parcial(self, entrega):
        if self._estado != EstadoEnvio.EN_TRANSITO:
            raise ValueError("Solo se pueden registrar entregas parciales con el envío en tránsito.")

        entrega.marcar_entregada()
        self._entregas_parciales.append(entrega)

        self.agregar_evento_historial(
            EventoHistorial(
                f"Entrega parcial registrada: {entrega.punto_entrega}",
                self._estado,
                self._estado
            )
        )

    def marcar_entregado(self):
        nuevo_estado = EstadoEnvio.ENTREGADO

        if not self.validar_transicion(nuevo_estado):
            raise ValueError("No se puede marcar como entregado desde el estado actual.")

        estado_anterior = self._estado
        self._estado = nuevo_estado

        self._vehiculo.cambiar_estado(EstadoVehiculo.DISPONIBLE)

        self.agregar_evento_historial(
            EventoHistorial(
                "Envío entregado",
                estado_anterior,
                nuevo_estado
            )
        )

    def cancelar(self):
        nuevo_estado = EstadoEnvio.CANCELADO

        if not self.validar_transicion(nuevo_estado):
            raise ValueError("No se puede cancelar el envío desde el estado actual.")

        estado_anterior = self._estado
        self._estado = nuevo_estado

        if self._vehiculo.estado_operativo == EstadoVehiculo.EN_RUTA:
            self._vehiculo.cambiar_estado(EstadoVehiculo.DISPONIBLE)

        self.agregar_evento_historial(
            EventoHistorial(
                "Envío cancelado",
                estado_anterior,
                nuevo_estado
            )
        )

    def agregar_evento_historial(self, evento):
        self._historial.append(evento)

    def obtener_historial(self):
        return self._historial

    def generar_reporte_historial(self):
        reporte = f"Historial del envío {self._numero_seguimiento}:\n"

        for evento in self._historial:
            reporte += f"- {evento.obtener_resumen()}\n"

        return reporte

    def to_dict(self):
        return {
            "numero_seguimiento": self._numero_seguimiento,
            "origen": self._origen.nombre,
            "destino": self._destino.nombre,
            "fecha_salida_programada": self._fecha_salida_programada,
            "fecha_llegada_estimada": self._fecha_llegada_estimada,
            "vehiculo": self._vehiculo.patente,
            "tipo_carga": self._tipo_carga.value,
            "estado": self._estado.value,
            "entregas_parciales": [
                entrega.to_dict() for entrega in self._entregas_parciales
            ],
            "historial": [
                evento.to_dict() for evento in self._historial
            ],
        }
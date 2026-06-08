from dominio.vehiculo import Vehiculo
from dominio.enums import TipoCarga

class VehiculoCargaPeligrosa(Vehiculo):
    def __init__(self, patente, marca, modelo, anio, habilitacion_peligrosa, estado_operativo=None):
        from dominio.enums import EstadoVehiculo
        if estado_operativo is None:
            estado_operativo = EstadoVehiculo.DISPONIBLE
        super().__init__(patente, marca, modelo, anio, estado_operativo)
        self._habilitacion_peligrosa = habilitacion_peligrosa

    @property
    def habilitacion_peligrosa(self):
        return self._habilitacion_peligrosa

    def obtener_tipo_carga(self):
        return TipoCarga.PELIGROSA

    def validar_carga(self, tipo_carga):
        return tipo_carga == TipoCarga.PELIGROSA and self.verificar_habilitacion()

    def verificar_habilitacion(self):
        return self._habilitacion_peligrosa is not None and self._habilitacion_peligrosa != ""

    def calcular_costo_envio(self, distancia_km):
        tarifa_por_km = 2000
        recargo_riesgo = 50000
        return distancia_km * tarifa_por_km + recargo_riesgo

    def generar_reporte(self):
        return (
            f"{super().generar_reporte()} - Tipo: Carga peligrosa - "
            f"Habilitación: {self._habilitacion_peligrosa}"
        )

    def to_dict(self):
        data = super().to_dict()
        data["habilitacion_peligrosa"] = self._habilitacion_peligrosa
        return data
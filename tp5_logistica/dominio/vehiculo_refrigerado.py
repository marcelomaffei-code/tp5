from dominio.vehiculo import Vehiculo
from dominio.enums import TipoCarga

class VehiculoRefrigerado(Vehiculo):
    def __init__(self, patente, marca, modelo, anio, temperatura_minima, estado_operativo=None):
        from dominio.enums import EstadoVehiculo
        if estado_operativo is None:
            estado_operativo = EstadoVehiculo.DISPONIBLE
        super().__init__(patente, marca, modelo, anio, estado_operativo)
        self._temperatura_minima = temperatura_minima

    @property
    def temperatura_minima(self):
        return self._temperatura_minima

    def obtener_tipo_carga(self):
        return TipoCarga.REFRIGERADA

    def validar_carga(self, tipo_carga):
        return tipo_carga == TipoCarga.REFRIGERADA

    def verificar_temperatura(self, temperatura_requerida):
        return temperatura_requerida >= self._temperatura_minima

    def calcular_costo_envio(self, distancia_km):
        tarifa_por_km = 1500
        recargo_refrigeracion = 20000
        return distancia_km * tarifa_por_km + recargo_refrigeracion

    def generar_reporte(self):
        return (
            f"{super().generar_reporte()} - Tipo: Vehículo refrigerado - "
            f"Temperatura mínima: {self._temperatura_minima}"
        )

    def to_dict(self):
        data = super().to_dict()
        data["temperatura_minima"] = self._temperatura_minima
        return data
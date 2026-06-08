from dominio.vehiculo import Vehiculo
from dominio.enums import TipoCarga

class CamionConvencional(Vehiculo):
    def obtener_tipo_carga(self):
        return TipoCarga.GENERAL

    def validar_carga(self, tipo_carga):
        return tipo_carga == TipoCarga.GENERAL

    def calcular_costo_envio(self, distancia_km):
        tarifa_por_km = 1000
        return distancia_km * tarifa_por_km

    def generar_reporte(self):
        return f"{super().generar_reporte()} - Tipo: Camión convencional - Carga: general"
from abc import ABC, abstractmethod
from dominio.enums import EstadoVehiculo, TipoCarga


class Vehiculo(ABC):
    def __init__(self, patente, marca, modelo, anio, estado_operativo=EstadoVehiculo.DISPONIBLE):
        self._patente = patente
        self._marca = marca
        self._modelo = modelo
        self._anio = anio
        self._estado_operativo = estado_operativo
        self._conductor = None
        self._mantenimientos = []

    @property
    def patente(self):
        return self._patente

    @property
    def estado_operativo(self):
        return self._estado_operativo

    @property
    def conductor(self):
        return self._conductor

    @property
    def mantenimientos(self):
        return self._mantenimientos

    def asignar_conductor(self, conductor):
        self._conductor = conductor

    def cambiar_estado(self, nuevo_estado):
        if not isinstance(nuevo_estado, EstadoVehiculo):
            raise ValueError("Estado de vehículo inválido.")
        self._estado_operativo = nuevo_estado

    def agregar_mantenimiento(self, intervencion):
        self._mantenimientos.append(intervencion)

    def esta_disponible(self):
        return self._estado_operativo == EstadoVehiculo.DISPONIBLE

    @abstractmethod
    def obtener_tipo_carga(self):
        pass

    @abstractmethod
    def validar_carga(self, tipo_carga):
        pass

    @abstractmethod
    def calcular_costo_envio(self, distancia_km):
        pass

    def generar_reporte(self):
        return (
            f"Vehículo {self._patente} - {self._marca} {self._modelo} "
            f"({self._anio}) - Estado: {self._estado_operativo.value}"
        )

    def to_dict(self):
        return {
            "tipo_clase": self.__class__.__name__,
            "patente": self._patente,
            "marca": self._marca,
            "modelo": self._modelo,
            "anio": self._anio,
            "estado_operativo": self._estado_operativo.value,
            "conductor_licencia": self._conductor.licencia if self._conductor else None,
            "mantenimientos": [m.to_dict() for m in self._mantenimientos],
        }


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


class VehiculoRefrigerado(Vehiculo):
    def __init__(self, patente, marca, modelo, anio, temperatura_minima, estado_operativo=EstadoVehiculo.DISPONIBLE):
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


class VehiculoCargaPeligrosa(Vehiculo):
    def __init__(self, patente, marca, modelo, anio, habilitacion_peligrosa, estado_operativo=EstadoVehiculo.DISPONIBLE):
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
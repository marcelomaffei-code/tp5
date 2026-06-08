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
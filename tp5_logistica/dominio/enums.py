from enum import Enum


class EstadoVehiculo(Enum):
    DISPONIBLE = "disponible"
    EN_MANTENIMIENTO = "en_mantenimiento"
    EN_RUTA = "en_ruta"


class EstadoEnvio(Enum):
    PENDIENTE = "pendiente"
    EN_TRANSITO = "en_transito"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class CategoriaConductor(Enum):
    NOVATO = "novato"
    EXPERIMENTADO = "experimentado"
    SENIOR = "senior"


class TipoCarga(Enum):
    GENERAL = "general"
    REFRIGERADA = "refrigerada"
    PELIGROSA = "peligrosa"


class EstadoEntregaParcial(Enum):
    PENDIENTE = "pendiente"
    ENTREGADA = "entregada"
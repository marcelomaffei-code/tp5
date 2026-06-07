from dominio.enums import CategoriaConductor, TipoCarga


class Conductor:
    def __init__(self, licencia, nombre, antiguedad, categoria):
        if not isinstance(categoria, CategoriaConductor):
            raise ValueError("Categoría de conductor inválida.")

        self._licencia = licencia
        self._nombre = nombre
        self._antiguedad = antiguedad
        self._categoria = categoria
        self._vehiculo_asignado = None

    @property
    def licencia(self):
        return self._licencia

    @property
    def nombre(self):
        return self._nombre

    @property
    def antiguedad(self):
        return self._antiguedad

    @property
    def categoria(self):
        return self._categoria

    @property
    def vehiculo_asignado(self):
        return self._vehiculo_asignado

    def puede_transportar(self, tipo_carga):
        if not isinstance(tipo_carga, TipoCarga):
            raise ValueError("Tipo de carga inválido.")

        puede = False

        if tipo_carga == TipoCarga.GENERAL:
            puede = True
        elif tipo_carga == TipoCarga.REFRIGERADA:
            puede = self._categoria in [
                CategoriaConductor.EXPERIMENTADO,
                CategoriaConductor.SENIOR
            ]
        elif tipo_carga == TipoCarga.PELIGROSA:
            puede = self._categoria == CategoriaConductor.SENIOR

        return puede

    def asignar_vehiculo(self, vehiculo):
        if not self.esta_disponible():
            raise ValueError("El conductor ya tiene un vehículo asignado.")

        self._vehiculo_asignado = vehiculo

    def liberar_vehiculo(self):
        self._vehiculo_asignado = None

    def esta_disponible(self):
        return self._vehiculo_asignado is None

    def generar_reporte(self):
        vehiculo = "Sin vehículo asignado"

        if self._vehiculo_asignado is not None:
            vehiculo = self._vehiculo_asignado.patente

        return (
            f"Conductor {self._nombre} - Licencia: {self._licencia} - "
            f"Categoría: {self._categoria.value} - Vehículo: {vehiculo}"
        )

    def to_dict(self):
        return {
            "licencia": self._licencia,
            "nombre": self._nombre,
            "antiguedad": self._antiguedad,
            "categoria": self._categoria.value,
            "vehiculo_patente": (
                self._vehiculo_asignado.patente
                if self._vehiculo_asignado is not None
                else None
            )
        }
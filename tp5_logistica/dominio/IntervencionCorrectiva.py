from dominio.mantenimiento import IntervencionMantenimiento

class IntervencionCorrectiva(IntervencionMantenimiento):
    def __init__(self, fecha, kilometraje, descripcion, costo_base, gravedad_falla):
        super().__init__(fecha, kilometraje, descripcion, costo_base)
        self._gravedad_falla = gravedad_falla

    @property
    def gravedad_falla(self):
        return self._gravedad_falla

    def obtener_tipo(self):
        return "correctiva"

    def calcular_costo_estimado(self):
        multiplicador = 1.0
        if isinstance(self._gravedad_falla, str):
            nivel = self._gravedad_falla.lower()
            if nivel == "media":
                multiplicador = 1.25
            elif nivel == "alta":
                multiplicador = 1.50
        return self._costo_base * multiplicador

    def generar_reporte(self):
        return (
            f"Mantenimiento correctivo - Fecha: {self._fecha} - "
            f"Km: {self._kilometraje} - "
            f"Descripción: {self._descripcion} - "
            f"Gravedad: {self._gravedad_falla} - "
            f"Costo estimado: {self.calcular_costo_estimado()}"
        )

    def to_dict(self):
        data = super().to_dict()
        data["gravedad_falla"] = self._gravedad_falla
        return data
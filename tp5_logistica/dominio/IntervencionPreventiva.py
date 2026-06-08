from dominio.mantenimiento import IntervencionMantenimiento

class IntervencionPreventiva(IntervencionMantenimiento):
    def __init__(self, fecha, kilometraje, descripcion, costo_base, revision_programada):
        super().__init__(fecha, kilometraje, descripcion, costo_base)
        self._revision_programada = revision_programada
        
    @property
    def revision_programada(self):
        return self._revision_programada

    def obtener_tipo(self):
        return "preventiva"

    def calcular_costo_estimado(self):
        recargo_programacion = 0
        if self._revision_programada:
            recargo_programacion = self._costo_base * 0.10
        return self._costo_base + recargo_programacion

    def generar_reporte(self):
        return (
            f"Mantenimiento preventivo - Fecha: {self._fecha} - "
            f"Km: {self._kilometraje} - "
            f"Descripción: {self._descripcion} - "
            f"Costo estimado: {self.calcular_costo_estimado()}"
        )

    def to_dict(self):
        data = super().to_dict()
        data["revision_programada"] = self._revision_programada
        return data
class CentroDistribucion:
    def __init__(self, nombre, ciudad, direccion, capacidad_maxima, personal_asignado):
        self._nombre = nombre
        self._ciudad = ciudad
        self._direccion = direccion
        self._capacidad_maxima = capacidad_maxima
        self._personal_asignado = personal_asignado
        self._envios_recibidos = []
        self._envios_despachados = []

    @property
    def nombre(self):
        return self._nombre

    @property
    def ciudad(self):
        return self._ciudad

    @property
    def direccion(self):
        return self._direccion

    @property
    def capacidad_maxima(self):
        return self._capacidad_maxima

    @property
    def personal_asignado(self):
        return self._personal_asignado

    @property
    def envios_recibidos(self):
        return self._envios_recibidos

    @property
    def envios_despachados(self):
        return self._envios_despachados

    def puede_recibir(self, cantidad):
        return cantidad <= self._capacidad_maxima

    def recibir_envio(self, envio):
        self._envios_recibidos.append(envio)

    def despachar_envio(self, envio):
        self._envios_despachados.append(envio)

    def generar_reporte(self):
        return (
            f"Centro: {self._nombre} - Ciudad: {self._ciudad} - "
            f"Capacidad máxima: {self._capacidad_maxima} - "
            f"Personal asignado: {self._personal_asignado}"
        )

    def to_dict(self):
        return {
            "nombre": self._nombre,
            "ciudad": self._ciudad,
            "direccion": self._direccion,
            "capacidad_maxima": self._capacidad_maxima,
            "personal_asignado": self._personal_asignado,
            "envios_recibidos": [
                envio.numero_seguimiento for envio in self._envios_recibidos
            ],
            "envios_despachados": [
                envio.numero_seguimiento for envio in self._envios_despachados
            ],
        }
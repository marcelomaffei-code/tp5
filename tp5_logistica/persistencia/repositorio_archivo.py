import json
import os

from persistencia.repositorio_datos import RepositorioDatos


class RepositorioArchivo(RepositorioDatos):
    def __init__(self, ruta_archivo):
        self._ruta_archivo = ruta_archivo

    @property
    def ruta_archivo(self):
        return self._ruta_archivo

    def existe_archivo(self):
        return os.path.exists(self._ruta_archivo)

    def guardar(self, datos):
        carpeta = os.path.dirname(self._ruta_archivo)

        if carpeta != "" and not os.path.exists(carpeta):
            os.makedirs(carpeta)

        with open(self._ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def cargar(self):
        datos = {}

        if self.existe_archivo():
            try:
                with open(self._ruta_archivo, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"El archivo de datos no tiene un formato JSON valido: {error}"
                ) from error
            except OSError as error:
                raise ValueError(
                    f"No se pudo leer el archivo de datos: {error}"
                ) from error

        if not isinstance(datos, dict):
            raise ValueError("El archivo de datos debe contener un objeto JSON principal.")

        return datos

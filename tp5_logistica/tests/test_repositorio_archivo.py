import json
import os
import tempfile
import unittest

from persistencia.repositorio_archivo import RepositorioArchivo


class RepositorioArchivoTest(unittest.TestCase):
    def test_cargar_devuelve_diccionario_vacio_si_no_existe_archivo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            repositorio = RepositorioArchivo(os.path.join(carpeta, "datos.json"))

            self.assertEqual({}, repositorio.cargar())

    def test_guardar_crea_carpeta_y_persiste_json(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "datos", "datos.json")
            repositorio = RepositorioArchivo(ruta)

            repositorio.guardar({"vehiculos": []})

            with open(ruta, "r", encoding="utf-8") as archivo:
                self.assertEqual({"vehiculos": []}, json.load(archivo))

    def test_cargar_rechaza_json_invalido(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "datos.json")
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write("{json invalido")

            repositorio = RepositorioArchivo(ruta)

            with self.assertRaisesRegex(ValueError, "formato JSON valido"):
                repositorio.cargar()

    def test_cargar_rechaza_json_que_no_es_objeto(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = os.path.join(carpeta, "datos.json")
            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump([], archivo)

            repositorio = RepositorioArchivo(ruta)

            with self.assertRaisesRegex(ValueError, "objeto JSON principal"):
                repositorio.cargar()


if __name__ == "__main__":
    unittest.main()

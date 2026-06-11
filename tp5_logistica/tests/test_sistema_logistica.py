import unittest

from dominio.enums import TipoCarga
from servicios.sistema_logistica import SistemaLogistica


class RepositorioMemoria:
    def __init__(self, datos=None):
        self.datos = datos if datos is not None else {}
        self.datos_guardados = None

    def cargar(self):
        return self.datos

    def guardar(self, datos):
        self.datos_guardados = datos


class SistemaLogisticaTest(unittest.TestCase):
    def crear_sistema_con_datos_de_prueba(self):
        sistema = SistemaLogistica(RepositorioMemoria())
        sistema.cargar_datos_de_prueba()
        return sistema

    def test_cargar_datos_de_prueba_es_idempotente(self):
        sistema = SistemaLogistica(RepositorioMemoria())

        sistema.cargar_datos_de_prueba()
        sistema.cargar_datos_de_prueba()

        self.assertEqual(3, len(sistema.vehiculos))
        self.assertEqual(3, len(sistema.conductores))
        self.assertEqual(3, len(sistema.centros))
        self.assertEqual("AB123CD", sistema.conductores["LIC001"].vehiculo_asignado.patente)

    def test_simular_flujo_completo_es_idempotente(self):
        sistema = SistemaLogistica(RepositorioMemoria())

        primer_envio = sistema.simular_flujo_completo()
        segundo_envio = sistema.simular_flujo_completo()

        self.assertIs(primer_envio, segundo_envio)
        self.assertEqual(["ENV001"], list(sistema.envios.keys()))

    def test_crear_envio_valida_formato_de_fechas(self):
        sistema = self.crear_sistema_con_datos_de_prueba()

        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            sistema.crear_envio(
                numero_seguimiento="ENV-FECHA",
                nombre_origen="Centro Buenos Aires",
                nombre_destino="Centro Córdoba",
                patente_vehiculo="AB123CD",
                fecha_salida_programada="11/06/2026",
                fecha_llegada_estimada="2026-06-12",
                tipo_carga=TipoCarga.GENERAL,
            )

    def test_crear_envio_rechaza_llegada_anterior_a_salida(self):
        sistema = self.crear_sistema_con_datos_de_prueba()

        with self.assertRaisesRegex(ValueError, "anterior a la salida"):
            sistema.crear_envio(
                numero_seguimiento="ENV-RANGO",
                nombre_origen="Centro Buenos Aires",
                nombre_destino="Centro Córdoba",
                patente_vehiculo="AB123CD",
                fecha_salida_programada="2026-06-12",
                fecha_llegada_estimada="2026-06-11",
                tipo_carga=TipoCarga.GENERAL,
            )

    def test_obtener_mantenimientos_rechaza_rango_de_fechas_invalido(self):
        sistema = self.crear_sistema_con_datos_de_prueba()

        with self.assertRaisesRegex(ValueError, "fecha hasta"):
            sistema.obtener_mantenimientos_por_periodo("2026-06-12", "2026-06-01")

    def test_cargar_datos_con_error_conserva_estado_anterior(self):
        sistema = self.crear_sistema_con_datos_de_prueba()
        sistema._repositorio = RepositorioMemoria({"centros": "no es una lista"})

        with self.assertRaisesRegex(ValueError, "No se pudieron cargar"):
            sistema.cargar_datos()

        self.assertEqual(3, len(sistema.vehiculos))
        self.assertEqual(3, len(sistema.conductores))
        self.assertEqual(3, len(sistema.centros))


if __name__ == "__main__":
    unittest.main()

from datetime import datetime

from dominio.enums import EstadoVehiculo, EstadoEnvio, CategoriaConductor, TipoCarga
from dominio.camion_convencional import CamionConvencional
from dominio.vehiculo_refrigerado import VehiculoRefrigerado
from dominio.vehiculo_carga_peligrosa import VehiculoCargaPeligrosa
from dominio.conductor import Conductor
from dominio.centro_distribucion import CentroDistribucion
from dominio.envio import Envio
from dominio.entrega_parcial import EntregaParcial
from dominio.evento_historial import EventoHistorial
from dominio.IntervencionPreventiva import IntervencionPreventiva
from dominio.IntervencionCorrectiva import IntervencionCorrectiva
from dominio.mantenimiento import mantenimiento_from_dict

class SistemaLogistica:
    def __init__(self, repositorio):
        self._vehiculos = {}
        self._conductores = {}
        self._centros = {}
        self._envios = {}
        self._repositorio = repositorio

    @property
    def vehiculos(self):
        return self._vehiculos

    @property
    def conductores(self):
        return self._conductores

    @property
    def centros(self):
        return self._centros

    @property
    def envios(self):
        return self._envios

    def registrar_vehiculo(self, vehiculo):
        if vehiculo.patente in self._vehiculos:
            raise ValueError("Ya existe un vehículo con esa patente.")

        self._vehiculos[vehiculo.patente] = vehiculo

    def registrar_conductor(self, conductor):
        if conductor.licencia in self._conductores:
            raise ValueError("Ya existe un conductor con esa licencia.")

        self._conductores[conductor.licencia] = conductor

    def registrar_centro(self, centro):
        if centro.nombre in self._centros:
            raise ValueError("Ya existe un centro con ese nombre.")

        self._centros[centro.nombre] = centro

    def asignar_conductor_a_vehiculo(self, licencia, patente):
        if licencia not in self._conductores:
            raise ValueError("No existe un conductor con esa licencia.")

        if patente not in self._vehiculos:
            raise ValueError("No existe un vehículo con esa patente.")

        conductor = self._conductores[licencia]
        vehiculo = self._vehiculos[patente]
        tipo_carga = vehiculo.obtener_tipo_carga()

        if not conductor.esta_disponible():
            raise ValueError("El conductor no está disponible.")

        if not vehiculo.esta_disponible():
            raise ValueError("El vehículo no está disponible.")

        if not conductor.puede_transportar(tipo_carga):
            raise ValueError("El conductor no puede transportar ese tipo de carga.")

        conductor.asignar_vehiculo(vehiculo)
        vehiculo.asignar_conductor(conductor)

    def crear_envio(
        self,
        numero_seguimiento,
        nombre_origen,
        nombre_destino,
        patente_vehiculo,
        fecha_salida_programada,
        fecha_llegada_estimada,
        tipo_carga,
    ):
        self._validar_fecha(fecha_salida_programada, "fecha de salida programada")
        self._validar_fecha(fecha_llegada_estimada, "fecha de llegada estimada")

        if fecha_llegada_estimada < fecha_salida_programada:
            raise ValueError("La fecha de llegada estimada no puede ser anterior a la salida.")

        if numero_seguimiento in self._envios:
            raise ValueError("Ya existe un envío con ese número de seguimiento.")

        if nombre_origen not in self._centros:
            raise ValueError("No existe el centro de origen.")

        if nombre_destino not in self._centros:
            raise ValueError("No existe el centro de destino.")

        if patente_vehiculo not in self._vehiculos:
            raise ValueError("No existe el vehículo indicado.")

        if not isinstance(tipo_carga, TipoCarga):
            raise ValueError("Tipo de carga inválido.")

        vehiculo = self._vehiculos[patente_vehiculo]

        if not vehiculo.esta_disponible():
            raise ValueError("El vehículo no está disponible.")

        if vehiculo.conductor is None:
            raise ValueError("El vehículo no tiene conductor asignado.")

        if not vehiculo.validar_carga(tipo_carga):
            raise ValueError("El vehículo no puede transportar ese tipo de carga.")

        if not vehiculo.conductor.puede_transportar(tipo_carga):
            raise ValueError("El conductor no puede transportar ese tipo de carga.")

        origen = self._centros[nombre_origen]
        destino = self._centros[nombre_destino]

        envio = Envio(
            numero_seguimiento=numero_seguimiento,
            origen=origen,
            destino=destino,
            fecha_salida_programada=fecha_salida_programada,
            fecha_llegada_estimada=fecha_llegada_estimada,
            vehiculo=vehiculo,
            tipo_carga=tipo_carga,
        )

        self._envios[numero_seguimiento] = envio
        origen.despachar_envio(envio)

        return envio

    def iniciar_envio(self, numero_seguimiento):
        envio = self._obtener_envio(numero_seguimiento)
        envio.iniciar_transito()

    def finalizar_envio(self, numero_seguimiento):
        envio = self._obtener_envio(numero_seguimiento)
        envio.marcar_entregado()
        envio.destino.recibir_envio(envio)

    def cancelar_envio(self, numero_seguimiento):
        envio = self._obtener_envio(numero_seguimiento)
        envio.cancelar()

    def registrar_entrega_parcial(self, numero_seguimiento, entrega):
        envio = self._obtener_envio(numero_seguimiento)
        envio.registrar_entrega_parcial(entrega)

    def registrar_mantenimiento(self, patente, intervencion):
        if patente not in self._vehiculos:
            raise ValueError("No existe un vehículo con esa patente.")

        vehiculo = self._vehiculos[patente]
        vehiculo.agregar_mantenimiento(intervencion)

    def obtener_historial_envio(self, numero_seguimiento):
        envio = self._obtener_envio(numero_seguimiento)
        return envio.generar_reporte_historial()

    def obtener_mantenimientos_por_periodo(self, fecha_desde, fecha_hasta):
        self._validar_fecha(fecha_desde, "fecha desde")
        self._validar_fecha(fecha_hasta, "fecha hasta")

        if fecha_hasta < fecha_desde:
            raise ValueError("La fecha hasta no puede ser anterior a la fecha desde.")

        resultados = []

        for vehiculo in self._vehiculos.values():
            for mantenimiento in vehiculo.mantenimientos:
                if fecha_desde <= mantenimiento.fecha <= fecha_hasta:
                    resultados.append((vehiculo, mantenimiento))

        return resultados

    def guardar_datos(self):
        datos = self._crear_datos_para_guardar()
        self._repositorio.guardar(datos)

    def cargar_datos(self):
        datos = self._repositorio.cargar()

        if datos:
            estado_anterior = (
                self._vehiculos,
                self._conductores,
                self._centros,
                self._envios,
            )

            try:
                self._vehiculos = {}
                self._conductores = {}
                self._centros = {}
                self._envios = {}

                centros_data = self._obtener_lista_datos(datos, "centros")
                conductores_data = self._obtener_lista_datos(datos, "conductores")
                vehiculos_data = self._obtener_lista_datos(datos, "vehiculos")
                envios_data = self._obtener_lista_datos(datos, "envios")

                self._cargar_centros(centros_data)
                self._cargar_conductores(conductores_data)
                self._cargar_vehiculos(vehiculos_data)
                self._cargar_asignaciones_conductores(conductores_data)
                self._cargar_envios(envios_data)
            except (KeyError, TypeError, ValueError) as error:
                (
                    self._vehiculos,
                    self._conductores,
                    self._centros,
                    self._envios,
                ) = estado_anterior
                raise ValueError(
                    f"No se pudieron cargar los datos guardados: {error}"
                ) from error

    def cargar_datos_de_prueba(self):
        camion = CamionConvencional("AB123CD", "Mercedes-Benz", "Atego", 2020)
        refrigerado = VehiculoRefrigerado("AC456EF", "Iveco", "Daily Refrigerado", 2021, -5)
        peligroso = VehiculoCargaPeligrosa("AD789GH", "Volvo", "FH", 2019, "HAZMAT-2026")

        conductor1 = Conductor("LIC001", "Juan Pérez", 1, CategoriaConductor.NOVATO)
        conductor2 = Conductor("LIC002", "Laura Gómez", 5, CategoriaConductor.EXPERIMENTADO)
        conductor3 = Conductor("LIC003", "Carlos Fernández", 12, CategoriaConductor.SENIOR)

        centro1 = CentroDistribucion("Centro Buenos Aires", "Buenos Aires", "Av. Logística 1500", 10000, 25)
        centro2 = CentroDistribucion("Centro Córdoba", "Córdoba", "Ruta Nacional 9 km 700", 8000, 18)
        centro3 = CentroDistribucion("Centro Rosario", "Rosario", "Av. Circunvalación 3200", 7000, 15)

        self._registrar_vehiculo_si_no_existe(camion)
        self._registrar_vehiculo_si_no_existe(refrigerado)
        self._registrar_vehiculo_si_no_existe(peligroso)

        self._registrar_conductor_si_no_existe(conductor1)
        self._registrar_conductor_si_no_existe(conductor2)
        self._registrar_conductor_si_no_existe(conductor3)

        self._registrar_centro_si_no_existe(centro1)
        self._registrar_centro_si_no_existe(centro2)
        self._registrar_centro_si_no_existe(centro3)

        self._asignar_si_corresponde("LIC001", "AB123CD")
        self._asignar_si_corresponde("LIC002", "AC456EF")
        self._asignar_si_corresponde("LIC003", "AD789GH")

    def simular_flujo_completo(self):
        self.cargar_datos_de_prueba()

        if "ENV001" in self._envios:
            return self._envios["ENV001"]

        envio = self.crear_envio(
            numero_seguimiento="ENV001",
            nombre_origen="Centro Buenos Aires",
            nombre_destino="Centro Córdoba",
            patente_vehiculo="AB123CD",
            fecha_salida_programada="2026-06-10",
            fecha_llegada_estimada="2026-06-12",
            tipo_carga=TipoCarga.GENERAL,
        )

        mantenimiento = IntervencionPreventiva(
            fecha="2026-06-05",
            kilometraje=85000,
            descripcion="Revisión general, cambio de aceite y control de frenos.",
            costo_base=120000,
            revision_programada=True,
        )
        mantenimiento_correctivo = IntervencionCorrectiva(
            fecha="2026-06-07",
            kilometraje=64000,
            descripcion="Reparacion del sistema de refrigeracion.",
            costo_base=250000,
            gravedad_falla="alta",
        )

        self.registrar_mantenimiento("AB123CD", mantenimiento)
        self.registrar_mantenimiento("AC456EF", mantenimiento_correctivo)

        self.iniciar_envio("ENV001")

        entrega = EntregaParcial(
            punto_entrega="Villa María",
            fecha_entrega="2026-06-11",
            detalle_carga="Entrega parcial de carga general.",
        )

        self.registrar_entrega_parcial("ENV001", entrega)
        self.finalizar_envio("ENV001")
        self.guardar_datos()

        return envio

    def _obtener_envio(self, numero_seguimiento):
        if numero_seguimiento not in self._envios:
            raise ValueError("No existe un envío con ese número de seguimiento.")

        return self._envios[numero_seguimiento]

    def _validar_fecha(self, fecha, nombre_campo):
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except (TypeError, ValueError) as error:
            raise ValueError(
                f"La {nombre_campo} debe tener formato YYYY-MM-DD."
            ) from error

    def _obtener_lista_datos(self, datos, clave):
        valor = datos.get(clave, [])

        if not isinstance(valor, list):
            raise ValueError(f"El campo '{clave}' debe ser una lista.")

        return valor

    def _registrar_vehiculo_si_no_existe(self, vehiculo):
        if vehiculo.patente not in self._vehiculos:
            self.registrar_vehiculo(vehiculo)

    def _registrar_conductor_si_no_existe(self, conductor):
        if conductor.licencia not in self._conductores:
            self.registrar_conductor(conductor)

    def _registrar_centro_si_no_existe(self, centro):
        if centro.nombre not in self._centros:
            self.registrar_centro(centro)

    def _asignar_si_corresponde(self, licencia, patente):
        if licencia not in self._conductores or patente not in self._vehiculos:
            return

        conductor = self._conductores[licencia]
        vehiculo = self._vehiculos[patente]

        if conductor.vehiculo_asignado is None and vehiculo.conductor is None:
            self.asignar_conductor_a_vehiculo(licencia, patente)

    def _crear_datos_para_guardar(self):
        return {
            "vehiculos": [vehiculo.to_dict() for vehiculo in self._vehiculos.values()],
            "conductores": [conductor.to_dict() for conductor in self._conductores.values()],
            "centros": [centro.to_dict() for centro in self._centros.values()],
            "envios": [envio.to_dict() for envio in self._envios.values()],
        }

    def _cargar_centros(self, centros_data):
        for data in centros_data:
            centro = CentroDistribucion(
                nombre=data["nombre"],
                ciudad=data["ciudad"],
                direccion=data["direccion"],
                capacidad_maxima=data["capacidad_maxima"],
                personal_asignado=data["personal_asignado"],
            )

            self._centros[centro.nombre] = centro

    def _cargar_conductores(self, conductores_data):
        for data in conductores_data:
            conductor = Conductor(
                licencia=data["licencia"],
                nombre=data["nombre"],
                antiguedad=data["antiguedad"],
                categoria=CategoriaConductor(data["categoria"]),
            )

            self._conductores[conductor.licencia] = conductor

    def _cargar_vehiculos(self, vehiculos_data):
        for data in vehiculos_data:
            estado = EstadoVehiculo(data["estado_operativo"])
            tipo_clase = data["tipo_clase"]

            if tipo_clase == "CamionConvencional":
                vehiculo = CamionConvencional(
                    data["patente"],
                    data["marca"],
                    data["modelo"],
                    data["anio"],
                    estado,
                )

            elif tipo_clase == "VehiculoRefrigerado":
                vehiculo = VehiculoRefrigerado(
                    data["patente"],
                    data["marca"],
                    data["modelo"],
                    data["anio"],
                    data["temperatura_minima"],
                    estado,
                )

            elif tipo_clase == "VehiculoCargaPeligrosa":
                vehiculo = VehiculoCargaPeligrosa(
                    data["patente"],
                    data["marca"],
                    data["modelo"],
                    data["anio"],
                    data["habilitacion_peligrosa"],
                    estado,
                )

            else:
                raise ValueError("Tipo de vehículo inválido al cargar datos.")

            for mantenimiento_data in data.get("mantenimientos", []):
                vehiculo.agregar_mantenimiento(
                    mantenimiento_from_dict(mantenimiento_data)
                )

            self._vehiculos[vehiculo.patente] = vehiculo

    def _cargar_asignaciones_conductores(self, conductores_data):
        for data in conductores_data:
            licencia = data["licencia"]
            patente = data.get("vehiculo_patente")

            if patente is not None and licencia in self._conductores and patente in self._vehiculos:
                conductor = self._conductores[licencia]
                vehiculo = self._vehiculos[patente]
                conductor.asignar_vehiculo(vehiculo)
                vehiculo.asignar_conductor(conductor)

    def _cargar_envios(self, envios_data):
        for data in envios_data:
            origen = self._centros[data["origen"]]
            destino = self._centros[data["destino"]]
            vehiculo = self._vehiculos[data["vehiculo"]]

            envio = Envio(
                numero_seguimiento=data["numero_seguimiento"],
                origen=origen,
                destino=destino,
                fecha_salida_programada=data["fecha_salida_programada"],
                fecha_llegada_estimada=data["fecha_llegada_estimada"],
                vehiculo=vehiculo,
                tipo_carga=TipoCarga(data["tipo_carga"]),
            )

            envio._estado = EstadoEnvio(data["estado"])
            envio._entregas_parciales = [
                EntregaParcial.from_dict(entrega_data)
                for entrega_data in data.get("entregas_parciales", [])
            ]
            envio._historial = [
                EventoHistorial.from_dict(evento_data)
                for evento_data in data.get("historial", [])
            ]

            self._envios[envio.numero_seguimiento] = envio

            origen.despachar_envio(envio)

            if envio.estado == EstadoEnvio.ENTREGADO:
                destino.recibir_envio(envio)

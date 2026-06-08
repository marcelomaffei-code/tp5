from dominio.enums import TipoCarga
from dominio.camion_convencional import CamionConvencional
from dominio.vehiculo_refrigerado import VehiculoRefrigerado
from dominio.vehiculo_carga_peligrosa import VehiculoCargaPeligrosa
from dominio.centro_distribucion import CentroDistribucion
from dominio.entrega_parcial import EntregaParcial
from dominio.mantenimiento import IntervencionPreventiva, IntervencionCorrectiva
from dominio.enums import CategoriaConductor
from dominio.conductor import Conductor

class MenuConsola:
    def __init__(self, sistema):
        self._sistema = sistema
        self._ejecutando = True

    def iniciar(self):
        print("Sistema de Gestión Logística")

        while self._ejecutando:
            self._mostrar_menu()
            opcion = input("Seleccione una opción: ")
            self._procesar_opcion(opcion)

    def _mostrar_menu(self):
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Registrar vehículo")
        print("2. Registrar conductor")
        print("3. Registrar centro de distribución")
        print("4. Crear envío")
        print("5. Asignar conductor a vehículo")
        print("6. Registrar mantenimiento")
        print("7. Registrar entrega parcial")
        print("8. Iniciar envío")
        print("9. Finalizar envío")
        print("10. Consultar historial de envío")
        print("11. Consultar mantenimientos por período")
        print("12. Guardar datos")
        print("13. Cargar datos")
        print("14. Simular flujo completo")
        print("15. Cargar datos de prueba")
        print("0. Salir")

    def _procesar_opcion(self, opcion):
        try:
            if opcion == "1":
                self._registrar_vehiculo()
            elif opcion == "2":
                self._registrar_conductor()
            elif opcion == "3":
                self._registrar_centro()
            elif opcion == "4":
                self._crear_envio()
            elif opcion == "5":
                self._asignar_conductor()
            elif opcion == "6":
                self._registrar_mantenimiento()
            elif opcion == "7":
                self._registrar_entrega_parcial()
            elif opcion == "8":
                self._iniciar_envio()
            elif opcion == "9":
                self._finalizar_envio()
            elif opcion == "10":
                self._consultar_historial()
            elif opcion == "11":
                self._consultar_mantenimientos()
            elif opcion == "12":
                self._sistema.guardar_datos()
                print("Datos guardados correctamente.")
            elif opcion == "13":
                self._sistema.cargar_datos()
                print("Datos cargados correctamente.")
            elif opcion == "14":
                envio = self._sistema.simular_flujo_completo()
                print("Simulación ejecutada correctamente.")
                print(envio.generar_reporte_historial())
            elif opcion == "15":
                self._sistema.cargar_datos_de_prueba()
                print("Datos de prueba cargados correctamente.")
            elif opcion == "0":
                self._ejecutando = False
                print("Saliendo del sistema...")
            else:
                print("Opción inválida.")
        except ValueError as error:
            print(f"Error: {error}")
        except Exception as error:
            print(f"Ocurrió un error inesperado: {error}")

    def _registrar_vehiculo(self):
        print("\nTipo de vehículo:")
        print("1. Camión convencional")
        print("2. Vehículo refrigerado")
        print("3. Vehículo de carga peligrosa")

        tipo = input("Seleccione tipo: ")
        patente = input("Patente: ")
        marca = input("Marca: ")
        modelo = input("Modelo: ")
        anio = int(input("Año: "))

        if tipo == "1":
            vehiculo = CamionConvencional(patente, marca, modelo, anio)
        elif tipo == "2":
            temperatura_minima = float(input("Temperatura mínima: "))
            vehiculo = VehiculoRefrigerado(
                patente,
                marca,
                modelo,
                anio,
                temperatura_minima
            )
        elif tipo == "3":
            habilitacion = input("Habilitación carga peligrosa: ")
            vehiculo = VehiculoCargaPeligrosa(
                patente,
                marca,
                modelo,
                anio,
                habilitacion
            )
        else:
            raise ValueError("Tipo de vehículo inválido.")

        self._sistema.registrar_vehiculo(vehiculo)
        print("Vehículo registrado correctamente.")

    def _registrar_conductor(self):
        licencia = input("Licencia: ")
        nombre = input("Nombre: ")
        antiguedad = int(input("Antigüedad: "))

        print("\nCategoría:")
        print("1. Novato")
        print("2. Experimentado")
        print("3. Senior")

        opcion = input("Seleccione categoría: ")
        categoria = self._obtener_categoria(opcion)

        conductor = Conductor(licencia, nombre, antiguedad, categoria)
        self._sistema.registrar_conductor(conductor)

        print("Conductor registrado correctamente.")

    def _registrar_centro(self):
        nombre = input("Nombre: ")
        ciudad = input("Ciudad: ")
        direccion = input("Dirección: ")
        capacidad = int(input("Capacidad máxima: "))
        personal = int(input("Personal asignado: "))

        centro = CentroDistribucion(nombre, ciudad, direccion, capacidad, personal)
        self._sistema.registrar_centro(centro)

        print("Centro de distribución registrado correctamente.")

    def _crear_envio(self):
        numero = input("Número de seguimiento: ")
        origen = input("Centro de origen: ")
        destino = input("Centro de destino: ")
        patente = input("Patente del vehículo: ")
        fecha_salida = input("Fecha salida programada: ")
        fecha_llegada = input("Fecha llegada estimada: ")

        print("\nTipo de carga:")
        print("1. General")
        print("2. Refrigerada")
        print("3. Peligrosa")

        opcion = input("Seleccione tipo de carga: ")
        tipo_carga = self._obtener_tipo_carga(opcion)

        self._sistema.crear_envio(
            numero_seguimiento=numero,
            nombre_origen=origen,
            nombre_destino=destino,
            patente_vehiculo=patente,
            fecha_salida_programada=fecha_salida,
            fecha_llegada_estimada=fecha_llegada,
            tipo_carga=tipo_carga
        )

        print("Envío creado correctamente.")

    def _asignar_conductor(self):
        licencia = input("Licencia del conductor: ")
        patente = input("Patente del vehículo: ")

        self._sistema.asignar_conductor_a_vehiculo(licencia, patente)

        print("Conductor asignado correctamente.")

    def _registrar_mantenimiento(self):
        patente = input("Patente del vehículo: ")

        print("\nTipo de mantenimiento:")
        print("1. Preventivo")
        print("2. Correctivo")

        tipo = input("Seleccione tipo: ")
        fecha = input("Fecha: ")
        kilometraje = int(input("Kilometraje: "))
        descripcion = input("Descripción: ")
        costo_base = float(input("Costo base: "))

        if tipo == "1":
            revision = input("¿Es revisión programada? s/n: ")
            revision_programada = revision.lower() == "s"

            mantenimiento = IntervencionPreventiva(
                fecha,
                kilometraje,
                descripcion,
                costo_base,
                revision_programada
            )
        elif tipo == "2":
            gravedad = input("Gravedad de falla baja/media/alta: ")

            mantenimiento = IntervencionCorrectiva(
                fecha,
                kilometraje,
                descripcion,
                costo_base,
                gravedad
            )
        else:
            raise ValueError("Tipo de mantenimiento inválido.")

        self._sistema.registrar_mantenimiento(patente, mantenimiento)

        print("Mantenimiento registrado correctamente.")

    def _registrar_entrega_parcial(self):
        numero = input("Número de seguimiento del envío: ")
        punto = input("Punto de entrega: ")
        fecha = input("Fecha de entrega: ")
        detalle = input("Detalle de carga: ")

        entrega = EntregaParcial(punto, fecha, detalle)
        self._sistema.registrar_entrega_parcial(numero, entrega)

        print("Entrega parcial registrada correctamente.")

    def _iniciar_envio(self):
        numero = input("Número de seguimiento del envío: ")
        self._sistema.iniciar_envio(numero)
        print("Envío iniciado correctamente.")

    def _finalizar_envio(self):
        numero = input("Número de seguimiento del envío: ")
        self._sistema.finalizar_envio(numero)
        print("Envío finalizado correctamente.")

    def _consultar_historial(self):
        numero = input("Número de seguimiento del envío: ")
        historial = self._sistema.obtener_historial_envio(numero)
        print(historial)

    def _consultar_mantenimientos(self):
        desde = input("Fecha desde YYYY-MM-DD: ")
        hasta = input("Fecha hasta YYYY-MM-DD: ")

        resultados = self._sistema.obtener_mantenimientos_por_periodo(desde, hasta)

        if not resultados:
            print("No se encontraron mantenimientos en el período indicado.")
        else:
            for vehiculo, mantenimiento in resultados:
                print(f"Vehículo: {vehiculo.patente}")
                print(mantenimiento.generar_reporte())

    def _obtener_categoria(self, opcion):
        categoria = None

        if opcion == "1":
            categoria = CategoriaConductor.NOVATO
        elif opcion == "2":
            categoria = CategoriaConductor.EXPERIMENTADO
        elif opcion == "3":
            categoria = CategoriaConductor.SENIOR
        else:
            raise ValueError("Categoría inválida.")

        return categoria

    def _obtener_tipo_carga(self, opcion):
        tipo_carga = None

        if opcion == "1":
            tipo_carga = TipoCarga.GENERAL
        elif opcion == "2":
            tipo_carga = TipoCarga.REFRIGERADA
        elif opcion == "3":
            tipo_carga = TipoCarga.PELIGROSA
        else:
            raise ValueError("Tipo de carga inválido.")

        return tipo_carga
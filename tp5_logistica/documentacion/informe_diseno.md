# Informe de decisiones de diseno

## Objetivo

El sistema implementa una gestion logistica por consola para registrar vehiculos, conductores, centros de distribucion, envios, entregas parciales y mantenimientos. La solucion esta organizada por modulos para separar dominio, servicios, interfaz y persistencia.

## Requisitos funcionales cubiertos

- Registro de vehiculos convencionales, refrigerados y de carga peligrosa.
- Registro de conductores con licencia, antiguedad y categoria.
- Validacion de tipos de carga segun vehiculo y categoria del conductor.
- Registro de centros de distribucion con direccion, capacidad y personal asignado.
- Creacion, inicio, finalizacion y cancelacion de envios.
- Registro de entregas parciales.
- Registro de mantenimientos preventivos y correctivos.
- Reporte de historial completo de un envio.
- Consulta de mantenimientos por periodo.
- Persistencia en archivo JSON.
- Ejecucion por consola, compatible con EC2 y Docker.

## Requisitos no funcionales considerados

- Mantenibilidad: el codigo esta separado en paquetes `dominio`, `servicios`, `persistencia` e `interfaz`.
- Bajo acoplamiento: `SistemaLogistica` depende de la abstraccion `RepositorioDatos`, lo que permite cambiar la persistencia sin modificar la logica principal.
- Alta cohesion: cada clase concentra responsabilidades propias del concepto que representa.
- Persistencia reemplazable: la implementacion actual usa `RepositorioArchivo`, pero se podria agregar otro repositorio.
- Sin variables globales para compartir estado: el estado se mantiene dentro de instancias.
- Herencia limitada: la jerarquia se mantiene corta y comprensible.

## Encapsulamiento

Los atributos principales son privados por convencion mediante prefijo `_`. El acceso se realiza con propiedades y metodos publicos. Las reglas de cambio de estado se concentran en metodos como `iniciar_transito`, `marcar_entregado`, `cancelar`, `asignar_conductor` y `registrar_entrega_parcial`.

## Herencia

La clase abstracta `Vehiculo` concentra informacion y comportamiento comun de la flota. Las clases `CamionConvencional`, `VehiculoRefrigerado` y `VehiculoCargaPeligrosa` especializan la validacion de carga y el calculo de costo. La clase abstracta `IntervencionMantenimiento` define el contrato de mantenimiento y las clases preventiva/correctiva implementan calculos particulares.

## Polimorfismo

El sistema usa polimorfismo en vehiculos y mantenimientos. Cada vehiculo responde a `validar_carga`, `obtener_tipo_carga` y `calcular_costo_envio` segun su tipo concreto. Cada intervencion responde a `calcular_costo_estimado` y `generar_reporte` segun sea preventiva o correctiva.

## Estructuras de datos

- Diccionarios para vehiculos, conductores, centros y envios, porque permiten busquedas directas por clave unica: patente, licencia, nombre de centro y numero de seguimiento.
- Listas para mantenimientos, entregas parciales e historial, porque conservan multiples elementos asociados a una entidad y permiten recorrerlos para reportes.
- Enumeraciones para estados, categorias y tipos de carga, porque evitan valores libres y reducen errores de validacion.

## Persistencia

La persistencia se realiza en `datos/datos_logistica.json`. Cada entidad relevante implementa `to_dict` y el servicio reconstruye objetos al cargar. El repositorio crea la carpeta de datos si no existe y guarda JSON con codificacion UTF-8.

## Deploy en AWS

El sistema es una aplicacion de consola. Por eso se propone ejecutarlo en una instancia EC2, directamente con Python o dentro de Docker. El archivo `AWS_DEPLOY.md` documenta los pasos de despliegue y ejecucion.

## Datos de prueba

El archivo `datos/datos_logistica.json` contiene un flujo completo con:

- 3 vehiculos.
- 3 conductores.
- 3 centros de distribucion.
- 1 envio entregado.
- 1 mantenimiento preventivo.
- 1 mantenimiento correctivo.
- 1 entrega parcial.
- Historial completo del envio.

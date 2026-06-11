# Documentacion CRC

## SistemaLogistica

Responsabilidades:
- Coordinar registros de vehiculos, conductores, centros y envios.
- Validar reglas de asignacion entre conductor, vehiculo y carga.
- Delegar persistencia en un repositorio.
- Exponer operaciones de consulta y auditoria.

Colaboradores:
- Vehiculo
- Conductor
- CentroDistribucion
- Envio
- RepositorioDatos

## Vehiculo

Responsabilidades:
- Mantener datos comunes de la flota.
- Controlar estado operativo.
- Registrar mantenimientos.
- Definir comportamiento polimorfico para tipo de carga y costo.

Colaboradores:
- Conductor
- IntervencionMantenimiento
- EstadoVehiculo

## CamionConvencional

Responsabilidades:
- Aceptar carga general.
- Calcular costo de envio para carga general.

Colaboradores:
- Vehiculo
- TipoCarga

## VehiculoRefrigerado

Responsabilidades:
- Aceptar carga refrigerada.
- Verificar temperatura minima.
- Calcular costo con recargo de refrigeracion.

Colaboradores:
- Vehiculo
- TipoCarga

## VehiculoCargaPeligrosa

Responsabilidades:
- Aceptar carga peligrosa si tiene habilitacion.
- Calcular costo con recargo por riesgo.

Colaboradores:
- Vehiculo
- TipoCarga

## Conductor

Responsabilidades:
- Mantener licencia, antiguedad y categoria.
- Informar si puede transportar un tipo de carga.
- Controlar asignacion actual a un unico vehiculo.

Colaboradores:
- Vehiculo
- CategoriaConductor
- TipoCarga

## CentroDistribucion

Responsabilidades:
- Mantener datos de ubicacion, capacidad y personal.
- Registrar envios despachados y recibidos.

Colaboradores:
- Envio

## Envio

Responsabilidades:
- Mantener datos de seguimiento, origen, destino, fechas, vehiculo y carga.
- Validar transiciones de estado.
- Registrar entregas parciales.
- Generar historial de auditoria.

Colaboradores:
- Vehiculo
- CentroDistribucion
- EntregaParcial
- EventoHistorial
- EstadoEnvio

## EntregaParcial

Responsabilidades:
- Registrar punto, fecha, detalle de carga y estado de la entrega parcial.

Colaboradores:
- EstadoEntregaParcial

## EventoHistorial

Responsabilidades:
- Registrar fecha, descripcion, estado anterior y estado nuevo de un evento.
- Generar resumen legible para auditoria.

Colaboradores:
- EstadoEnvio

## IntervencionMantenimiento

Responsabilidades:
- Mantener datos comunes de una intervencion.
- Definir operaciones polimorficas de tipo, costo y reporte.

Colaboradores:
- Vehiculo

## IntervencionPreventiva

Responsabilidades:
- Calcular costo de una revision preventiva.
- Indicar si la revision fue programada.

Colaboradores:
- IntervencionMantenimiento

## IntervencionCorrectiva

Responsabilidades:
- Calcular costo segun gravedad de falla.

Colaboradores:
- IntervencionMantenimiento

## RepositorioDatos

Responsabilidades:
- Definir contrato de guardado y carga.

Colaboradores:
- SistemaLogistica

## RepositorioArchivo

Responsabilidades:
- Persistir datos en un archivo JSON.
- Reconstruir datos desde el archivo.

Colaboradores:
- RepositorioDatos

# Historias de usuario

## Gestion de flota

- Como operador logistico quiero registrar vehiculos con patente, marca, modelo, anio y estado para administrar la flota disponible.
- Como operador logistico quiero diferenciar camiones convencionales, refrigerados y de carga peligrosa para validar que cada envio use el vehiculo correcto.
- Como responsable de mantenimiento quiero registrar intervenciones preventivas y correctivas para auditar el estado de cada vehiculo.

## Gestion de conductores

- Como operador logistico quiero registrar conductores con licencia, antiguedad y categoria para asignarlos a vehiculos.
- Como operador logistico quiero validar la categoria del conductor frente al tipo de carga para evitar asignaciones no permitidas.
- Como operador logistico quiero que un conductor solo tenga un vehiculo asignado al mismo tiempo para evitar conflictos operativos.

## Gestion de envios

- Como operador logistico quiero crear envios con numero de seguimiento, origen, destino y fechas para controlar el traslado de mercancias.
- Como operador logistico quiero cambiar el estado de un envio entre pendiente, en transito, entregado o cancelado para reflejar su situacion real.
- Como operador logistico quiero registrar entregas parciales para envios que reparten carga en varios puntos.

## Auditoria y persistencia

- Como auditor quiero consultar el historial completo de un envio para conocer cada cambio desde su creacion hasta su entrega.
- Como auditor quiero consultar mantenimientos por periodo para revisar que vehiculos fueron intervenidos.
- Como usuario del sistema quiero guardar y cargar datos desde archivos para conservar la informacion entre ejecuciones.
- Como docente evaluador quiero ejecutar el sistema en una maquina virtual EC2 para verificar su funcionamiento por consola.

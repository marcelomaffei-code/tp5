# Despliegue en AWS

Este proyecto es una aplicacion de consola interactiva. La forma mas simple de subirlo a AWS es ejecutarlo en una instancia EC2 y entrar por SSH para usar el menu.

## Opcion recomendada: EC2 con Docker

1. Crear una instancia EC2 con Ubuntu.
2. Abrir el puerto 22 solo para tu IP.
3. Conectarse por SSH:

```bash
ssh -i "C:\Users\Administrador\Downloads\tp_logistica_key.pem" ubuntu@3.21.167.26
```

4. Instalar Docker:

```bash
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
```

5. Cerrar y volver a entrar por SSH para que tome el grupo `docker`.
6. Subir el proyecto a la instancia. Desde tu maquina local:

```bash
scp -i "C:\Users\Administrador\Downloads\tp_logistica_key.pem" -r tp5_logistica ubuntu@3.21.167.26:/home/ubuntu/
```

7. Construir la imagen:

```bash
cd /home/ubuntu/tp5_logistica
docker build -t tp5-logistica .
```

8. Ejecutar la aplicacion con datos persistentes:

```bash
docker run --rm -it -v tp5_logistica_datos:/app/datos tp5-logistica
```

## Ejecutar sin Docker

Tambien se puede ejecutar directamente en EC2:

```bash
sudo apt update
sudo apt install -y python3
cd /home/ubuntu/tp5_logistica
python3 main.py
```

## Nota importante

Servicios como AWS App Runner, ECS o Elastic Beanstalk estan pensados para aplicaciones web o APIs que escuchan por HTTP. Como este proyecto usa `input()` y menu por consola, no es ideal para esos servicios sin antes convertir la interfaz en una web/API.

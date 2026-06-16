

```bash
ssh -i "C:\Users\Administrador\Downloads\tp_logistica_key.pem" ubuntu@18.190.159.185
```

Si Windows rechaza la clave con `UNPROTECTED PRIVATE KEY FILE`, ajustar permisos:

```powershell
icacls "C:\Users\Administrador\Downloads\tp_logistica_key.pem" /inheritance:r
icacls "C:\Users\Administrador\Downloads\tp_logistica_key.pem" /remove "MININT-TSBENE\CodexSandboxUsers"
icacls "C:\Users\Administrador\Downloads\tp_logistica_key.pem" /grant:r "${env:USERNAME}:R"
```

Luego volver a intentar el SSH.

4. Instalar Docker:

```bash
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
```

5. Cerrar y volver a entrar por SSH para que tome el grupo `docker`.
6. Subir el proyecto a la instancia. Desde tu maquina local:

```bash
ssh -i "C:\Users\Administrador\Downloads\tp_logistica_key.pem" ubuntu@18.190.159.185 "sudo rm -rf /home/ubuntu/tp5_logistica && mkdir -p /home/ubuntu/tp5_logistica && sudo chown -R ubuntu:ubuntu /home/ubuntu/tp5_logistica"
scp -i "C:\Users\Administrador\Downloads\tp_logistica_key.pem" -r . ubuntu@18.190.159.185:/home/ubuntu/tp5_logistica/
```

7. Construir la imagen:

```bash
cd /home/ubuntu/tp5_logistica
ls -l persistencia/repositorio_archivo.py
docker build --no-cache -t tp5-logistica .
```

8. Ejecutar la aplicacion con datos persistentes:

```bash
docker run --rm -it -v tp5_logistica_datos:/app/datos tp5-logistica
```

Si aparece `ModuleNotFoundError: No module named 'persistencia.repositorio_archivo'`, la instancia puede estar construyendo una copia vieja/incompleta del proyecto o la imagen puede tener permisos incorrectos en las carpetas copiadas. Verificar en EC2:

```bash
cd /home/ubuntu/tp5_logistica
find . -maxdepth 2 -type f | sort
ls -l persistencia/
docker run --rm tp5-logistica python -c "import os; print(os.listdir('/app/persistencia'))"
```

La salida debe incluir `persistencia/repositorio_archivo.py`. Si aparece `Permission denied`, confirmar que el Dockerfile tenga `chmod -R a+rX /app` antes de `USER appuser`, volver a subir el proyecto y reconstruir con `docker build --no-cache -t tp5-logistica .`.

## Ejecutar sin Docker

Tambien se puede ejecutar directamente en EC2:

```bash
sudo apt update
sudo apt install -y python3
cd /home/ubuntu/tp5_logistica
python3 main.py
```


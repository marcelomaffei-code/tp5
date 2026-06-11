FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# copiar todo el proyecto
COPY . /app

# instalar dependencias si existe requirements.txt
RUN if [ -f /app/requirements.txt ]; then pip install --no-cache-dir -r /app/requirements.txt; fi

# crear usuario no-root y ajustar permisos del proyecto
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser || true
RUN chmod -R a+rX /app && mkdir -p /app/datos && chown -R appuser:appgroup /app/datos
USER appuser

VOLUME ["/app/datos"]

CMD ["python", "main.py"]

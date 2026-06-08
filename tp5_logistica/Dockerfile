FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# copiar todo el proyecto
COPY . /app

# instalar dependencias si existe requirements.txt
RUN if [ -f /app/requirements.txt ]; then pip install --no-cache-dir -r /app/requirements.txt; fi

# crear usuario no-root (opcional)
RUN groupadd --system appgroup && useradd --system --gid appgroup appuser || true
USER appuser

CMD ["python", "main.py"]
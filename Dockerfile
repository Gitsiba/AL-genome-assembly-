# Lightweight container for reproducible assembly-metric plotting and pipeline diagrams.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLBACKEND=Agg

RUN apt-get update \
    && apt-get install -y --no-install-recommends graphviz \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY plot_assembly /app/plot_assembly
COPY out_lay /app/out_lay
COPY assembly_metrics_template.csv /app/assembly_metrics_template.csv

WORKDIR /work

# Plot actual metrics supplied from the mounted working directory.
ENTRYPOINT ["python", "/app/plot_assembly"]
CMD ["--help"]

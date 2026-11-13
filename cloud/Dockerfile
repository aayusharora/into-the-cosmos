# One image, two entry points: the scheduled report (a service) and the
# batch search (a job). Same code, same tools — only how you start it differs.
FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements-cloud.txt .
RUN pip install --no-cache-dir -r requirements-cloud.txt

COPY demo/ ./demo/
COPY cloud/ ./cloud/

# lightkurve caches MAST downloads here; mount a volume or accept cold starts.
ENV LIGHTKURVE_CACHE_DIR=/tmp/lightkurve

# Default is the batch worker. The scheduled service overrides this:
#   gcloud run deploy ... --command python --args demo/sky_report.py
CMD ["python", "cloud/search_worker.py"]

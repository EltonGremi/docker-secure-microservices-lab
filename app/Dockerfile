FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

COPY --chown=appuser:appgroup app.py .

USER appuser
EXPOSE 8000

CMD ["python", "app.py"]

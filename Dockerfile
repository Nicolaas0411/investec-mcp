FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

ARG PORT=8050
ENV PORT=$PORT

CMD ["python", "src/main.py"]
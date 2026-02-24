FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml requirements.txt README.md ./
COPY biblewise/ ./biblewise/

RUN pip install --no-cache-dir -e .

RUN python -m biblewise.fetch_bible

CMD ["biblewise"]

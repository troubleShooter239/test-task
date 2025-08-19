FROM python:3.13.7-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libmagic1 && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "src.main"]

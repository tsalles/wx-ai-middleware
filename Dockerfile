FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x run.sh

EXPOSE 8000

ENTRYPOINT ["sh", "./run.sh"]

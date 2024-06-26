FROM python:3.10-slim

WORKDIR /aiohttp_server

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "server.py"]
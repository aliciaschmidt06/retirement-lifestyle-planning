FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY * .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]

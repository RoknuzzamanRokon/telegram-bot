FROM python:3.11.6-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80


CMD ["python", "./auto-text.py"]

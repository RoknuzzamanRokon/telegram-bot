FROM python:3.12-slim

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --deploy --ignore-pipfile

COPY . .

CMD ["pipenv", "run", "python", "auto-text.py"]

FROM python:3.8.4

ENV PYTHONUNBUFFERED 1

EXPOSE 4422
WORKDIR /src

COPY poetry.lock pyproject.toml ./
RUN apt-get -y install --no-install-recommends make=* && \
    pip install poetry==1.2.1 && \
    poetry config virtualenvs.create false && \
    poetry install

COPY ./waterdip/ ./waterdip

ENTRYPOINT ["python", "-m", "waterdip"]
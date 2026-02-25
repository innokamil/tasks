FROM python:3.13-slim as base 
RUN apt-get update && apt-get install -y \
	    gcc \
	    g++ \
	    libpq-dev \
	    python3-dev 

RUN pip install poetry
RUN apt-get clean  

FROM base as dev
WORKDIR /code
ENV ROOT_DIRECTORY=/code 
ENV RESOURCES_DIRECTORY="${ROOT_DIRECTORY}/resources"
ENV PYTHONUNBUFFERED=1
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
COPY . .
ENTRYPOINT ["poetry"]
CMD ["run", "python", "app.py"]

FROM python:3.9.0-slim-buster

WORKDIR /web

COPY . /web


RUN pip install poetry

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "home_page.py"]
FROM python:3.8

RUN pip install pipenv
WORKDIR /usr/src/hetic_converteo
COPY Pipfile .
RUN pipenv install
COPY app ./
COPY data ./
COPY .streamlit ./
ENTRYPOINT ["pipenv", "run", "streamlit", "run", "app/streamlit.py"]
FROM python:3.8

ENV WORKDIR="/usr/project/hetic_converteo"
WORKDIR $WORKDIR
COPY Pipfile Pipfile.lock $WORKDIR/
COPY app $WORKDIR/app
COPY data $WORKDIR/data
COPY src $WORKDIR/src
COPY .streamlit $WORKDIR/.streamlit
RUN pip install pipenv && pipenv install --system
FROM python:3.8

RUN pip install pipenv

ENV WORKDIR="/usr/project/hetic_converteo"
WORKDIR $WORKDIR
COPY Pipfile $WORKDIR/.
RUN pipenv install
COPY app $WORKDIR/app
COPY data $WORKDIR/data
COPY src $WORKDIR/src
COPY .streamlit $WORKDIR/.streamlit

CMD ["pipenv", "run", "streamlit", "run", "$WORKDIR/app/🏘️Home.py"]
FROM python:3.8-slim-buster
LABEL maintainer="HETIC"
ENV WORKDIR="/usr/project/hetic_converteo"
WORKDIR $WORKDIR
COPY Pipfile Pipfile.lock $WORKDIR/
COPY src $WORKDIR/src
COPY .streamlit $WORKDIR/.streamlit
RUN pip install pipenv && pipenv install --system
# Remove "--server.port $PORT" for local run this docker image
# "--server.port $PORT" here is specific for Heroku
CMD streamlit run $WORKDIR/src/frontend/🏘️Home.py --server.port $PORT
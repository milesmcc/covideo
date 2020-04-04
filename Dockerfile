FROM python:3

WORKDIR /usr/src/covideo

RUN apt update
RUN apt install ffmpeg -y

RUN pip install pipenv
COPY Pipfile.lock ./
COPY Pipfile ./
RUN pipenv install --system --deploy

COPY covideo .

RUN python manage.py compilescss
RUN python manage.py collectstatic --noinput

ARG GF_UID="500"
ARG GF_GID="500"

# add group & user
RUN groupadd -r -g $GF_GID appgroup && \
   useradd appuser -r -u $GF_UID -g appgroup

USER appuser

EXPOSE 8080

CMD [ "./webserver.sh" ]
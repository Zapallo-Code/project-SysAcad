FROM python:3.12.10-bookworm

ENV FLASK_CONTEXT=production
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/sysacad/.local/bin

RUN useradd --create-home --home-dir /home/sysacad sysacad
RUN apt-get update
RUN apt-get install -y python3-dev build-essential libpq-dev python3-psycopg2
RUN apt-get install -y curl htop iputils-ping
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /home/sysacad

USER sysacad
RUN mkdir app

COPY ./app ./app
COPY ./app.py .

ADD requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]
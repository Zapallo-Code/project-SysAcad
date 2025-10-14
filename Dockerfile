FROM python:3.12.10-bookworm

ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/sysacad/.local/bin

RUN useradd --create-home --home-dir /home/sysacad sysacad
RUN apt-get update && \
    apt-get install -y python3-dev build-essential libpq-dev && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/sysacad

USER sysacad
RUN mkdir app

COPY --chown=sysacad:sysacad ./app ./app
COPY --chown=sysacad:sysacad ./main ./main
COPY --chown=sysacad:sysacad ./manage.py .
COPY --chown=sysacad:sysacad ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
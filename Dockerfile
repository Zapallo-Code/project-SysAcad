FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH=$PATH:/home/sysacad/.local/bin

RUN useradd --create-home --home-dir /home/sysacad sysacad

RUN apt-get update && \
    apt-get install -y python3-dev build-essential libpq-dev \
    libglib2.0-0 libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/sysacad

USER sysacad

COPY --chown=sysacad:sysacad requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=sysacad:sysacad . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
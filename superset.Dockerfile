# superset.Dockerfile
FROM apache/superset:latest
COPY ./backend/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py
USER root
RUN pip install flask-cors psycopg2-binary
USER superset
RUN superset db upgrade

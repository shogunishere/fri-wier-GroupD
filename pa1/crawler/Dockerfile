FROM postgres:12.18

ENV POSTGRES_PASSWORD=passwd
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=govcrawler

# Copy db_init.sql into the docker image
COPY db_init.sql /docker-entrypoint-initdb.d/

VOLUME ["/var/lib/postgresql/data", "/db"]

EXPOSE 5432

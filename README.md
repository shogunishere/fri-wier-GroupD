## Docker PostgreSQL database setup

0. Create ```.env``` file with following content:

```
DB_HOST=localhost
DB_USER=postgres
DB_NAME=govcrawler
DB_PASSWORD=psswd
DB_PORT=5432
```

1. Create empty ```pg_data``` directory, this is the mount volume for Docker.

2. Create and start container:
```docker run --name govcrawler -e POSTGRES_PASSWORD=psswd -e POSTGRES_USER=postgres -e POSTGRES_DB=govcrawler -v ${PWD}/pgdata:/var/lib/postgresql/data -v ${PWD}/db:/docker-entrypoint-initdb.d -p 5432:5432 -d postgres:12.2```

3. Copy init script to container:
```docker cp ./db/crawldb.sql govcrawler:/docker-entrypoint-initdb.d/crawldb.sql```

4. Create database in the container:
```docker exec -it govcrawler createdb -U postgres govcrawler```

5. Execute initialization SQL script:
   ```docker exec -it govcrawler psql -U postgres -d govcrawler -f /docker-entrypoint-initdb.d/crawldb.sql```

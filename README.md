## DB Setup

0. Create ```.env``` file with following content:

```
DB_HOST=localhost
DB_USER=postgres
DB_NAME=govcrawler
DB_PASSWORD=psswd
DB_PORT=5432
```

1. Create empty ```pg_data``` directory

2. ```docker exec -it govcrawler bash```

3. ```psql -U postgres```

4. ```CREATE DATABASE govcrawler;```

If you want to inspect remember to use: ```\c govcrawler``` before querying tables.

5. ```docker cp ./db/crawldb.sql govcrawler:/docker-entrypoint-initdb.d/crawldb.sql```

6. ```docker run --name govcrawler -e POSTGRES_PASSWORD=psswd -e POSTGRES_USER=postgres -e POSTGRES_DB=govcrawler -v ${PWD}/pgdata:/var/lib/postgresql/data -v ${PWD}/db:/docker-entrypoint-initdb.d -p 5432:5432 -d postgres:12.2```

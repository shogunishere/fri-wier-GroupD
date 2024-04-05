1. Create a virtual Python environment and install required packags (requirements.txt)

2. Download init SQL data file from mega (link in /db) and put in root 

3. Create the following .env file:

```
ENV POSTGRES_PASSWORD=passwd
ENV POSTGRES_USER=postgres
ENV POSTGRES_DB=govcrawler
```

4. Build Docker image and run it (database container)

5. Run the crawler with ```python ./src/main.py```


Contact us if there are any issues.
# Dockerize MySQL


## Run mysql server in docker

```bash
docker pull mysql
docker run -p 12345:3306 -e MYSQL_ROOT_PASSWORD=root --restart=no mysql
```

## Make a connection

```bash
mysql -h localhost -P 12345 --protocol=tcp -u root -p  
# root
```

## Query MySQL server

```sql
SELECT NOW();
```

```console
+---------------------+
| now()               |
+---------------------+
| 2023-02-13 09:23:09 |
+---------------------+
1 row in set (0.00 sec)
```
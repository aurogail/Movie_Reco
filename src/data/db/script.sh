pg_dump -h postgres-db -U admin -W -F c recofilm_db > recofilm_gdrive.sql

pg_restore -h postgres-db -U admin -d recofilm_db -F c recofilm_gdrive.sql


# if recofilm_db not created
pg_restore -U admin -d recofilm_db -C -F c var/lib/postgresql/data/recofilm_gdrive.sql

# if recofilm_db created
pg_restore -U admin -d recofilm_db -F c var/lib/postgresql/data/recofilm_gdrive.sql

pg_restore -U admin -d recofilm_db -F c var/lib/postgresql/data/recofilm_gdrive.sql

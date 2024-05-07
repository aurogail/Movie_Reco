pg_dump -U admin -W -F c recofilm_db > var/lib/postgresql/data/recofilm_db_backup.sql

# if recofilm_db not created
pg_restore -U admin -d recofilm_db -C -F c var/lib/postgresql/data/recofilm_db_backup.sql

# if recofilm_db created
pg_restore -U admin -d recofilm_db -F c var/lib/postgresql/data/recofilm_db_backup.sql
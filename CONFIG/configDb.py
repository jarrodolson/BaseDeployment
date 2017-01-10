import psycopg2
import hashlib
import random
import string

temp = ''.join(
    random.SystemRandom().choice(
        string.ascii_uppercase + string.digits) for _ in range(25))
print(temp)

hexDigest = hashlib.md5(temp.encode('utf-8')).hexdigest()
with open("sensitive_db_pass.txt", "w", encoding="utf-8") as fi:
    fi.write(hexDigest)

print(hexDigest)

with open("sensitive_db_pass_postgres.txt", "r") as fi:
	dbpass = fi.read().strip()
conn = psycopg2.connect("dbname=postgres user=postgres password={0}".format(dbpass))
conn.autocommit = True
cur = conn.cursor()

cur.execute("CREATE ROLE macmanus WITH CREATEDB PASSWORD %s;", (hexDigest,))
cur.execute("CREATE DATABASE saints OWNER macmanus;")
cur.execute(
    '''
    CREATE TABLE docs (
        id integer PRIMARY KEY DEFULT nextval('serial'),
        timestamp TIMEZONE WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
        finame text,
        doc_string text
        );
    '''
    )

import psycopg2
import hashlib
import random
import string
import argparse

parser = argparse.ArgumentParser(description="Set up a database")
parser.add_argument('tblname', help="Name of table to be created.")
args = parser.parse_args()
tblName = args.tblname

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

#cur.execute("CREATE ROLE macmanus WITH CREATEDB PASSWORD %s;", (hexDigest,))
#cur.execute("CREATE DATABASE saints OWNER macmanus;")
#cur.execute("DROP TABLE {0};".format(tblName))
cur.execute(
    '''
    CREATE TABLE {0} (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT clock_timestamp(),
        finame text,
        doc_string text
        );
    '''.format(tblName)
    )
cur.execute("ALTER TABLE {0} ADD COLUMN fts tsvector;".format(tblName))
cur.execute("UPDATE {0} SET fts = to_tsvector('english', doc_string);".format(tblName))
cur.execute("CREATE INDEX fts_idx ON {0} USING GIN (fts);".format(tblName))
cur.execute('''
    CREATE TRIGGER ftsvectorupdate BEFORE INSERT OR UPDATE
        ON {0} FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(fts, 'pg_catalog.english', doc_string);
    '''.format(tblName)
    )
    


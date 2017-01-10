import psycopg2

conn = psycopg2.connect("dbname=postgres user=postgres password=NBFegQ59")
conn.autocommit = True
cur = conn.cursor()

cur.execute("DROP DATABASE saints;")
cur.execute("DROP ROLE macmanus;")

import PyPDF2
import re
import psycopg2

reTag = re.compile("[0-9]{4}")

fi = open('data/SPSA-2017-Preliminary-Program-v4.pdf', 'rb')
obj = PyPDF2.PdfFileReader(fi)
print(obj.getDocumentInfo())
print(obj.getFields())
print(obj.getNumPages())
pages = []
chunks = []
for p in obj.pages[2:len(obj.pages)]:
    txt = p.extractText().replace("\n", "")
    tagLi = reTag.findall(txt)
    #print(tagLi)
    txtLi = reTag.split(txt)
    for i, t in enumerate(tagLi):
        if i == 0:
            chunks.append(('',t,))
        else:
            chunks.append((t, txtLi[i+1],))
    pages.append(txt)
fi.close()

chunks = [chunk for chunk in chunks if chunk[1].strip()!=""]
chunks = [chunk for chunk in chunks if chunk[0].strip()!=""]

with open("../sensitive_db_pass_postgres.txt", "r") as fi:
	dbpass = fi.read().strip()
conn = psycopg2.connect("dbname=postgres user=postgres password={0}".format(dbpass))
conn.autocommit = True
cur = conn.cursor()
cur.execute("ALTER TABLE docs ADD COLUMN session text;")
for chunk in chunks:
    cur.execute(
        '''
        INSERT INTO docs (finame, doc_string, session)
            VALUES ('nofile.txt', %s, %s);
        ''', (chunk[1], chunk[0]))

'''Script for reading in and analyzing dataset'''
import psycopg2
import spacy
import gensim

def ftsSearch(cur, keyword):
    '''Uses indexed content in database to return results with word'''
    cur.execute('''
        SELECT id, doc_string, session, 
        ts_rank_cd(fts, query) AS rank 
            FROM docs, plainto_tsquery('english', %s) query
            WHERE query @@ fts
            ORDER BY rank DESC
            LIMIT 10;
        ''', (keyword,))
    data = cur.fetchall()
    return data

def organizeEnts(docLi):
    '''Takes a list of parsed objects, and returns a list of dictioary items of same objects'''
    master = {}
    for d in docLi:
        for ent in d.ents:
            try:
                temp = master[ent.label_]
                try:
                    temp[ent.text]+=1
                except KeyError:
                    temp[ent.text] = 1
                master[ent.label_] = temp
            except KeyError:
                master[ent.label_] = {ent.text: 1}
    return master
    

with open("../sensitive_db_pass_postgres.txt", "r") as fi:
	dbpass = fi.read().strip()
conn = psycopg2.connect("dbname=postgres user=postgres password={0}".format(dbpass))
conn.autocommit = True
cur = conn.cursor()
#result = ftsSearch(cur, 'Jarrod Olson')
cur.execute("SELECT * FROM docs;")
result = cur.fetchall()

##Read in to a spacy setup
texts = [r[3] for r in result]
nlp = spacy.load('en')

docLi = [x for x in nlp.pipe(texts, batch_size=50, n_threads=2)]
entsLi = organizeEnts(docLi)

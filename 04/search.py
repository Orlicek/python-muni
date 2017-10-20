import json
import sys

import sqlite3

conn = sqlite3.connect('scorelib.dat')
cur = conn.cursor()
search = sys.argv[1]

sql_get_composers = """SELECT person.id, person.name FROM person
WHERE person.name LIKE ?"""

sql = """SELECT person.name,
score.genre, score.key, score.incipit, score.year,
print.id, print.partiture
FROM person JOIN score_author ON person.id = score_author.composer
JOIN score ON score.id = score_author.score
JOIN edition ON score.id = edition.score
JOIN print ON edition.id = print.edition
WHERE person.id = ?"""

cur.execute(sql_get_composers, ('%'+search+'%', ))


composer_list = []
for person_row in cur:
    person = {}
    person['composer_id'] = person_row[0]
    person['composer'] = person_row[1]
    composer_list.append(person)

#    person['score'] = {}
#    person['score']['genre'] = person_row[3]
#    person['score']['key'] = person_row[4]
#    person['score']['incipit'] = person_row[5]
#    person['score']['year'] = person_row[6]
#    person['print'] = {}
#    person['print']['id'] = person_row[7]
#    person['print']['partiture'] = person_row[8]

for person in person_list:
    cur.execute(sql_get_composers, (person.get('id'), ))
    person 

json.dump(composer_list, sys.stdout, indent=4)

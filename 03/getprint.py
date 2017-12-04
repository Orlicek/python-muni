import sqlite3
import json
import sys

sql = """SELECT person.name, person.born, person.died FROM person JOIN score_author ON person.id = score_author.composer
JOIN score ON score_author.score = score.id
JOIN edition ON score.id = edition.score
JOIN print ON edition.id = print.edition
where print.id = ?"""

con = sqlite3.connect('scorelib.dat')
cur = con.cursor()
search_print = sys.argv[1]
cur.execute(sql, (search_print,))

person_list = []
for row in cur:
    person = {}
    person['name'] = row[0]
    person['born'] = row[1]
    person['died'] = row[2]
    person_list.append(person)

json.dump(person_list, sys.stdout, indent=4)


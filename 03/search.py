import json
import sys

import sqlite3

conn = sqlite3.connect('scorelib.dat')
cur = conn.cursor()
search = sys.argv[1]

sql_get_composers = """SELECT person.id, person.name FROM person
WHERE person.name LIKE ?"""

sql_get_score = """SELECT
score.id, score.genre, score.key, score.incipit, score.year
FROM person JOIN score_author ON person.id = score_author.composer
JOIN score ON score.id = score_author.score
WHERE person.id = ?"""

sql_get_print = """SELECT
print.id, print.partiture FROM score
JOIN edition ON score.id = edition.score
JOIN print ON edition.id = print.edition
WHERE score.id = ?"""


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


for composer in composer_list:
    composer['scores'] = []
    cur.execute(sql_get_score, (composer.get('composer_id'), ))
    for score_row in cur:
        score = {}
        score_id = score_row[0]
        score['genre'] = score_row[1]
        score['key'] = score_row[2]
        score['incipit'] = score_row[3]
        score['year'] = score_row[4]
        score['print'] = []
        cur.execute(sql_get_print, (score_id,))
        for print_row in cur:
            print_dict = {}
            print_dict['partiture'] = print_row[1]
            score['print'].append(print_dict)
        composer['scores'].append(score)


json.dump(composer_list, sys.stdout, indent=4)

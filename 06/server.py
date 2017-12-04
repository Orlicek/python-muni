import os
from urllib.parse import urlparse, parse_qs
import http.client
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import json
import sys
import sqlite3


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


class MineBaseHTTPRequestHandler(BaseHTTPRequestHandler):
    print_partial = "<b>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Partiture: </b>%s"
    score_partial = """<b>&nbsp&nbsp&nbsp&nbsp Genre: </b>%s</br>
        <b>&nbsp&nbsp&nbsp&nbsp Key: </b>%s</br>
        <b>&nbsp&nbsp&nbsp&nbsp Incipit: </b>%s</br>
        <b>&nbsp&nbsp&nbsp&nbsp Year: </b>%s</br>
        <b>&nbsp&nbsp&nbsp&nbsp Prints: </b></br>%s</br>
    """
    composer_partial = """<b>Name: </b>%s</br>
        <b>Scores: </b></br>%s</br>
    """
    form = """<form action="./result" method="get">
        <input type="text" name="q" value=""></input>
        <input type="hidden" name="f" value="html"></input>
        <input type="submit" value="Submit" /> 
    </form>
    """
    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        if path == '/':
            self.send_response(200, "OK")
            self.send_header('Content-type','text-html')
            self.end_headers()
            self.wfile.write(bytes(self.form, encoding='UTF-8'))

        elif path == '/result':
            search = query.get('q')
            if search:
                search = search[0]
            resp_type = query.get('f', None)
            if resp_type:
                resp_type = resp_type[0]
            composer_list = self.find_composers(search)

            if resp_type == 'json':
                self.send_response(200, "OK")
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                output = json.dumps(composer_list)
                self.wfile.write(bytes(output, encoding='UTF-8'))
                return
            elif resp_type == 'html':
                output_html = ""
                self.send_response(200, "OK")
                self.send_header('Content-type','text-html')
                self.end_headers()
                for composer in composer_list:
                    name = composer.get('composer'),
                    scores = composer.get('scores')
                    score_html = '' 
                    for score in scores:
                        prints = score.get('print')
                        print_html = ''
                        for one_print in prints:
                            print_html += self.print_partial%one_print.get('partiture')
                        score_html += self.score_partial%(
                            score.get('genre'),
                            score.get('key'),
                            score.get('incipit'),
                            score.get('year'),
                            print_html
                        ) 
                    output_html += self.composer_partial%(
                        composer.get('composer'),
                        score_html
                    )
                                    
                self.wfile.write(bytes(output_html, encoding='UTF-8'))
                return
        return


    def find_composers(self, search):
        conn = sqlite3.connect('scorelib.dat')
        cur = conn.cursor()
        cur.execute(sql_get_composers, ('%'+search+'%', ))
        composer_list = []
        for person_row in cur:
            person = {}
            person['composer_id'] = person_row[0]
            person['composer'] = person_row[1]
            composer_list.append(person)

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
    
        return composer_list


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def run():
  print('http server is starting...')

  server_address = ('127.0.0.1', 8000)
  httpd = HTTPServer(server_address, MineBaseHTTPRequestHandler)
  print('http server is running...')
  httpd.serve_forever()
  
if __name__ == '__main__':
  run()

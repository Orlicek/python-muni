import re # regular expressions
import sqlite3

# This is a base class for objects that represent database items. It implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).

class DBItem:
    def __init__( self, conn ):
        self.id = None
        self.cursor = conn.cursor()

    def store( self ):
        self.fetch_id()
        if ( self.id is None ):
            self.do_store()
            self.cursor.execute( "select last_insert_rowid()" )
            self.id = self.cursor.fetchone()[ 0 ]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.

class Person( DBItem ):
    def __init__( self, conn, string ):
        super().__init__( conn )
        self.born = self.died = None
        self.name = re.sub( '\([0-9/+-]+\)', '', string ).strip()
        # NB. The code below was part of the exercise (extracting years of birth & death
        # from the string).
        m = re.search( "([0-9]+)--([0-9]+)", string )
        if not m is None:
            self.born = int( m.group( 1 ) )
            self.died = int( m.group( 2 ) )

    # TODO: Update born/died if the name is already present but has null values for
    # those fields. We assume that names are unique (not entirely true in practice).
    def fetch_id( self ):
        self.cursor.execute( "select id from person where name = ?", (self.name,) )

        # NB. The below lines had a bug in the original version of
        # scorelib-import.py (which however only becomes relevant when you
        # start implementing the Score class).
        res = self.cursor.fetchone()
        if not res is None: # TODO born/died update should be done inside this if
            self.id = res[ 0 ]

    def do_store( self ):
        print ("storing '%s'" % self.name)
        # NB. Part of the exercise was adding the born/died columns to the below query.
        self.cursor.execute( "insert into person (name, born, died) values (?, ?, ?)",
                             ( self.name, self.born, self.died ) )

class ScoreAuthor(DBItem):
    def __init__( self, conn, data):
        super().__init__( conn )

        self.genre = data.get('genre')
        self.key = data.get('key')
        self.incipit = data.get('incipit')
        self.year = data.get('composition year')

    def fetch_id( self ):
        self.cursor.execute( "select id from score where genre = {0} and key = {1} and incipit = {2} and year = {3} ?".format(self.genre, self.key, self.incipit, self.year) )

        res = self.cursor.fetchone()
        if not res is None: # TODO born/died update should be done inside this if
            self.id = res[ 0 ]

    def do_store( self ):
        print ("storing '%s'" % self.name)
        self.cursor.execute( "insert into score (key, incipit, year) values (?, ?, ?)",
                             ( self.key, self.incipit, self.year ) )


class Voice(DBItem):
    def __init__( self, conn, data):
        super().__init__( conn )

        self.number = data.get('number')
        self.score_id = data.get('score')
        self.name = data.get('name')

    def fetch_id( self ):
        sql = "select id from voice where number = {0} and name = {1}".format(self.number, self.name)
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        if not res is None:
            self.scores = res.score
            if self.score_id not in res.score:
                self.scores.append(self.score_id)
            self.id = res[0]

    def do_store( self ):
        print ("storing '%s'" % self.name)
        self.cursor.execute( "insert into voice (name, number, score) values (?, ?, ?)",
                             ( self.name, self.number, [self.scores] ) )

class Edition(DBItem):
    def __init__( self, conn, data):
        super().__init__( conn )

        self.score_id = data.get('score')
        self.name = data.get('name')
        self.year = data.get('year')

    def fetch_id( self ):
        self.cursor.execute( "select id from edition where name = ? and year = ?", (self.name, self.year) )

        res = self.cursor.fetchone()
        if not res is None: # TODO born/died update should be done inside this if
            self.scores = res.score
            if self.score_id not in res.score:
                self.scores.append(self.score_id)
            self.id = res[ 0 ]

    def do_store( self ):
        print ("storing '%s'" % self.name)
        self.cursor.execute( "insert into edition (name, year) values (?, ?)",
                             ( self.name, self.year ) )


class ScoreAuthor(DBItem):
    def __init__( self, conn, data):
        super().__init__( conn )

        self.genre = data.get('genre')
        self.key = data.get('key')
        self.incipit = data.get('incipit')
        self.year = data.get('composition year')

    def fetch_id( self ):
        self.cursor.execute( "select id from score where genre = {0} and key = {1} and incipit = {2} and year = {3} ?".format(self.genre, self.key, self.incipit, self.year) )

        res = self.cursor.fetchone()
        if not res is None: # TODO born/died update should be done inside this if
            self.id = res[ 0 ]

    def do_store( self ):
        print ("storing '%s'" % self.name)
        self.cursor.execute( "insert into score (key, incipit, year) values (?, ?, ?)",
                             ( self.key, self.incipit, self.year ) )

class EditionAuthor(DBItem):
    def __init__( self, conn, edition_id, editors):
        super().__init__( conn )

        self.edition = data.get('Genre')
        self.editors = data.get('Key')

    def fetch_id( self ):
        self.cursor.execute( "select id from edition_author where edition = ?", (self.edition))

        res = self.cursor.fetchone()
        if not res is None: # TODO born/died update should be done inside this if
            self.editors = self.editors + res.editor
            self.id = res[ 0 ]

    def do_store( self ):
        print ("storing '%s'" % self.name)
        self.cursor.execute( "insert into score (key, incipit, year) values (?, ?, ?)",
                             ( self.key, self.incipit, self.year ) )


class Print(DBItem):
    def __init__( self, conn, data, edition_id):
        super().__init__( conn )

        self.partiture = data.get('partiture')
        self.id = data.get('number')
        self.edition_id = edition_id

    def fetch_id( self ):
        self.cursor.execute( "select edition from print where id = ?", (self.id), )
        res = self.cursor.fetchone()
        if not res is None:
            self.editions = res.edition
            if self.edition_id not in res.edition:
                self.editions.append(edition_id)
            self.id = res[ 0 ]


    def do_store( self ):
        print ("storing '%s'" % self.name)
        self.cursor.execute( "insert into score (partiture, edition, id) values (?, ?, ?)",
                             ( self.partiture, self.editions, self.id ) )



# Process a single line of input.
def process(k, v, data):
    if k == 'Composer':
        for c in v.split(';'):
            data['composers'].append({
                'name': c.strip()
            }
    elif k in 'Genre', 'Key', 'Incipit', 'Composition Year':
        data['score'][k.lower()] = v
    elif k[:5] == 'Voice':
        k_split = k.split(' ')
        k = k_split[0].strip()
        num = k_split[1].strip()
        for name in v.split(','):
            data['voices'].append({
                'number': num,
                'name': name.strip()
            })
    elif k == 'Edition':
        data['edition']['name'] = v
    elif k == 'Editor':
        for c in v.split(';'):
            data['editors'].append({
                    'name': c.strip()
                })
    elif k == 'Publication Year':
        data['edition']['year'] = v
    elif k == 'Print Number':
        data['print']['id'] = v
    elif k == 'Partiture':
        v = v.strip()
        partiture = 'N'
        if 'partial' in v:
            partiture = 'P'
        elif 'yes' in v:
            partiture = 'Y'
        data['print']['partiture'] = partiture

def init_data(data):
    data = None{
        'voices': [],
        'score': {},
        'edition': {},
        'composers': [],
        'print': {}
        'editors': [],
    }
		

# Database initialisation: sqlite3 scorelib.dat ".read scorelib.sql"
conn = sqlite3.connect( 'scorelib.dat' )
rx = re.compile( r"(.*): (.*)" )
data = None
init_data(data)

for line in open( 'scorelib.txt', 'r', encoding='utf-8' ):
    m = rx.match( line )
    if m is None:
        score = Score(conn, data.get('score'))
        score.store()

        persons = []
        for person_data in data.get('composers'):
            person = Person(conn, person_data.get('name'))
            person.store()
            persons.append(person.id)

        for voice_data in data.get('voices'):
            voice = Voice(conn, score.id, voice_data)
            voice.store()

        editors = []
        for editor_data in data.get('editors'):
            person = Person(conn, editor_data.get('name'))
            person.store()
            editors.append(person.id)


        edition = Edition(conn, score.id, data.get('edition'))
        edition.store()

        score_author = ScoreAuthor(conn, score.id, persons)
        score.author.store()

        edition_author = EditionAuthor(conn, edition.id, persons)
        edition_author.store()


        
        init_data(data)
        continue
    process(m.group( 1 ), m.group( 2 ), data)
	

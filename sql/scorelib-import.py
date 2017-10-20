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

class Score(DBItem):
    def __init__( self, conn ):
        super().__init__( conn )
	
    def set_genre(self, genre):
        self.genre = genre
	
    def set_key(self, key):
        self.key = key
	
    def set_incipit(self, incipit):
        self.incipit = incipit
	
    def set_year(self, year):
        self.year = year

    # TODO: Update born/died if the name is already present but has null values for
    # those fields. We assume that names are unique (not entirely true in practice).
    def fetch_id( self ):
        self.cursor.execute( "select id from score where genre = {0} and key = {1} and incipit = {2} and year = {3} ?".format(self.genre, self.key, self.incipit, self.year) )

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



key = None
genre = None
Incipit = None
comp_year = None

# Process a single line of input.
def process(k, v, score):
    if k == 'Composer':
        for c in v.split(';'):
            p = Person(conn, c.strip())
            p.store()
    elif k == 'Genre':
        score.set_genre(v)
    elif k == 'Key':
        score.set_key(v)
    elif k == 'Incipit':
        score.set_incipit(v)
    elif k == 'Composition Year':
        score.set_year(v)
		
	

# Database initialisation: sqlite3 scorelib.dat ".read scorelib.sql"
conn = sqlite3.connect( 'scorelib.dat' )
score = Score(conn)
rx = re.compile( r"(.*): (.*)" )
for line in open( 'scorelib.txt', 'r', encoding='utf-8' ):
    m = rx.match( line )
    if m is None:
        score.store()
        score = Score(conn)
        continue
    process( m.group( 1 ), m.group( 2 ), score)
	

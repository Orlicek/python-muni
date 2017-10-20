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
        self.name = re.sub( '\([0-9+-]+\)', '', string )
        # TODO: years born/died

    def fetch_id( self ):
        self.cursor.execute( "select id from person where name = ?", (self.name,) )
        res = self.cursor.fetchone()
        if res is not None:
            self.id = res [ 0 ]

    def do_store( self ):
        self.cursor.execute( "insert into person (name) values (?)", (self.name,) )

class Score(DBItem):
	def __init__(self, conn, string):
		pass


f = open('scorelib.txt', 'r', encoding='utf-8')
composer_r = re.compile(r"Composer:(.*)")
editor_r = re.compile(r"Editor:(.*)")
conn = sqlite3.connect('./scorelib.dat')
for line in f:
	# composer
	composer_match = re.match(composer_r,line)
	if composer_match is not None:
		composers_name = composer_match.group(1)
		for composer_name in composers_name.split(';') :
			composer = Person(conn, composer_name.strip())
			composer.store()

	#editor
	editor_match = re.match(editor_r, line)
	if editor_match is not None:
		continue
	editors_name = editor_match.group(1)

	for editor_name in editors_name.split(';'):
		editor = Person(conn, editor_name.strip())
		editor.store()


conn.commit()

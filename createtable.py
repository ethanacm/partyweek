SQLLITE = 'database.db'
conn = sqlite3.connect(SQLLITE)
c = conn.cursor()
c.execute('''
CREATE TABLE "database" (
	"timestamp"	INTEGER,
	"amount"	INTEGER NOT NULL DEFAULT 0,
	"year"	TEXT,
	"username"	TEXT,
	"caption"	TEXT,
	PRIMARY KEY("timestamp")
);
''')
conn.close()
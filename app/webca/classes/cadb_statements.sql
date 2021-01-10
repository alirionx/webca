CREATE TABLE "authorities" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"created"	TEXT,
	"contact"	TEXT,
	"comment"	TEXT,
	"key"	TEXT,
	"cert"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);


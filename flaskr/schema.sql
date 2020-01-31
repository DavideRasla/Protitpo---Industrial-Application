/*DROP TABLE IF EXISTS user;*/
/*DROP TABLE IF EXISTS post;*/

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uname TEXT NOT NULL,
  ulast TEXT NOT NULL,
  email TEXT NOT NULL,
  premium TEXT,
  profession TEXT,
  birthday TEXT ,
  addr TEXT ,
  social TEXT ,
  interest TEXT ,
  music TEXT,
  voiceid TEXT,
  faceid TEXT,
  sx TEXT
);

/*CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);*/
DROP TABLE IF EXISTS players;

CREATE TABLE players (
  name     TEXT,
  function TEXT,
  goals    INTEGER,
  league   TEXT
);

INSERT INTO players VALUES
('Messi',   'attack',   25, 'spanish'),
('Ribeiro', 'midfield', 21, 'spanish'),
('Oscar',   'midfield', 15, 'spanish'),
('Soares',  'attack',   14, 'spanish'),
('Silva',   'defense',   9, 'brazilian');

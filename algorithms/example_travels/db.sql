DROP TABLE IF EXISTS travels;

CREATE TABLE travels (
  destination TEXT,
  price       INTEGER,
  duration    INTEGER,
  itinerary   TEXT
);

INSERT INTO travels VALUES
('Angra'         , 2000, 4, 'cruise'),
('Buzios'        , 2000, 5, 'beach'),
('Salvador'      , 2600, 6, 'cruise'),
('Belo Horizonte', 2700, 5, 'urban'),
('Rio de Janeiro', 2600, 7, 'beach');

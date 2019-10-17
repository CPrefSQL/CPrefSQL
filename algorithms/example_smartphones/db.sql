DROP TABLE IF EXISTS smartphones;

CREATE TABLE smartphones (
    brand   TEXT,
    model   TEXT,
    ram     FLOAT,
    storage FLOAT,
    screen  FLOAT, 
    price   INTEGER
);

INSERT INTO smartphones VALUES
('Apple',    'Iphone X',      3.0,  64.0, 5.8, 4600),
('Samsung',  'Galaxy S10',    8.0, 128.0, 6.1, 3200),
('Samsung',  'Galaxy Note 9', 6.0, 128.0, 6.4, 2600),
('Xiaomi',   'MI 9',          6.0,  64.0, 6.4, 2200),
('Samsung',  'Galaxy S8',     4.0,  64.0, 5.8, 2300),
('Motorola', 'Moto X4',       3.0,  32.0, 5.2, 1400);

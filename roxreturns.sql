--
-- Table structure for table Market
--

DROP TABLE IF EXISTS Market;

CREATE TABLE Market (
item_id serial PRIMARY KEY,
item_make varchar(50),
item_model varchar(50),
item_year int,
item_location int,
item_price numeric(8,2)
);

--
-- Dumping data for table Market
--

INSERT INTO Market (item_make, item_model, item_year, item_location, item_price)
VALUES 
('Pontiac','LeMans (Convertible)',1972,20170,10999),
('Pontiac','GTO',2006,22030,16500),
('Pontiac','GTO',1970,23235,8500),
('Pontiac','GTO',1969,20772,8500),
('Pontiac','LeMans (Wagon)',1978,22401,6500),
('Pontiac','Fiero',1988,22401,3500),
('Pontiac','TransAm',1980,22401,1100),
('Pontiac','TransAm WS6',2001,22401,12500);


--
-- Table structure for table Members
--

DROP TABLE IF EXISTS Members;

CREATE TABLE Members (member_id serial PRIMARY KEY, first_name varchar(50) NOT NULL, last_name varchar(50) NOT NULL, email varchar(50) NOT NULL, zipcode int NOT NULL, YEAR int, model varchar(30) DEFAULT '', password text DEFAULT 'pontiac');

--
-- Dumping data for table Members
--

INSERT INTO Members (first_name, last_name, email, zipcode, YEAR, model, password)
VALUES ( 'pontiac',
         'app tester',
         'fake_email@fake_email.gl',
         22401,
         1971,
         'Pontiac GTO (hardtop)',
         crypt('pontiac', gen_salt('bf')));

INSERT INTO Members (first_name, last_name, email, zipcode, YEAR, model)
VALUES ( 'Jacques',
         'Troussard',
         'jacques@some-email.com',
         22401,
         1971,
         'Pontiac GTO (hardtop)');


INSERT INTO members
VALUES (DEFAULT,
        'Michael',
        'Hendrey',
        'mikey@some-email.com',
        94596,
        1970,
        'Chevrolet Chevelle');


INSERT INTO members
VALUES (DEFAULT,
        'Zelco',
        'Cecich',
        'zel-cab@email.com',
        94597,
        1955,
        'Chevrolet 3100s');


INSERT INTO members
VALUES (DEFAULT,
        'Grant',
        'Thornton',
        'punkrocker@email.com',
        94590,
        1953,
        'Chevrolet 210 Wagon');


INSERT INTO members
VALUES (DEFAULT,
        'Christine',
        'Kappa',
        'racer_girl@email.com',
        94566,
        1967,
        'Chevrolet Camaro');


INSERT INTO members
VALUES (DEFAULT,
        'Emily',
        'Romanova',
        'eroma@email.com',
        10033,
        1965,
        'Pontiac GTO (hardtop)');


INSERT INTO members
VALUES (DEFAULT,
        'Xaiver',
        'Zander',
        'triplex@staremail.com',
        10123,
        1967,
        'Pontiac GTO (hardtop)');
        
GRANT SELECT ON members, market TO webapp;
GRANT INSERT ON members TO webapp;
GRANT ALL ON market_item_id_seq, members_member_id_seq TO webapp;
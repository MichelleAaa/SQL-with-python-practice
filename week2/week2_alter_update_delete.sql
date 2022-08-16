-- Instructions:
-- Test your code as you go by running the following command from your VS Code integrated terminal:
-- cat week2_alter_update_delete.sql | docker exec -i pg_container psql
-- After running this command, refresh or open pgAdmin in your browser at http://localhost:5433 , then navigate to the database 


-- kill other connections
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'week2_alter_update_delete' AND pid <> pg_backend_pid();
-- (re)create the database
DROP DATABASE IF EXISTS week2_alter_update_delete;
CREATE DATABASE week2_alter_update_delete;
-- connect via psql
\c week2_alter_update_delete

-- database configuration
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET default_tablespace = '';
SET default_with_oids = false;


---
--- CREATE tables
---

CREATE TABLE divisions (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    name TEXT NOT NULL UNIQUE,
    home_color TEXT NOT NULL,
    away_color TEXT,
    division_id INT
);


---
--- Add foreign key constraints
---

ALTER TABLE teams 
ADD CONSTRAINT fk_teams_divisions 
FOREIGN KEY (division_id) 
REFERENCES divisions (id) 
ON DELETE SET NULL;

---
--- Insert Entries into the Database
---

INSERT INTO divisions (name) VALUES 
('Atlantic'), ('Metropolitan'), ('Pacific'), ('Central');
INSERT INTO teams (city, name, home_color, away_color, division_id) VALUES 
('New York', 'Islanders', 'Royal blue', 'White', 2),
('Seattle', 'Kraken', 'Deep sea blue', 'White', 3);

---
--- Update a Record
---

UPDATE divisions set name = 'Cosmopolitan' 
WHERE name = 'Metropolitan';

---
--- Delete a Record
---

DELETE FROM divisions WHERE name = 'Cosmopolitan';
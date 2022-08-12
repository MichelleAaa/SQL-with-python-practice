CREATE TABLE categories (
    id SERIAL,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    picture TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE products (
    id SERIAL,
    name TEXT NOT NULL,
    discontinued BOOLEAN NOT NULL,
    category_id INT,
    PRIMARY KEY (id)
);


ALTER TABLE products
ADD CONSTRAINT fk_products_categories
FOREIGN KEY (category_id)
REFERENCES categories;


-- In the week1 folder, open a terminal and enter:
-- docker ps
-- You should see output regarding the Container ID, etc.
-- cd .. (go back to the main file folder)
-- docker compose up -d
-- cd week1 

-- cat week1_script.sql | docker exec -i pg_container psql -d week1
-- •	This command basically says: "Inside the Docker container named pg_container, use psql to connect to the database named week1, and feed it the contents of the file week1_script.sql as input".

-- you should be able to refresh the pgAdmin page at http://localhost:5433 to see the new tables.

DROP DATABASE IF EXISTS warehouse_project

CREATE DATABASE warehouse_project;

\c warehouse_project

CREATE TABLE employee(
    user_name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE warehouse(
    id integer PRIMARY KEY,
    name VARCHAR (50)
);

CREATE TABLE item(
    state VARCHAR (100),
    category VARCHAR (100),
    warehouse integer REFERENCES warehouse(id),
    date_of_stock timestamp
);

SELECT COUNT(*)
FROM item
WHERE category = 'Smartühone';

SELECT COUNT(*)
FROM item
WHERE state = 'Blue' AND warehouse = '1';

SELECT w.name, COUNT(*) AS count
FROM warehouse w
JOIN item i ON w.id = i.warehouse
GROUP BY w.name
ORDER BY count DESC;




# Script to import book data, in a CSV file, into a database, using INSERT INTO command from SQL

##Fields of CSV
This Python script is used to import book data from a CSV file into a MySQL database. The CSV file must contain the following fields:

tb_collection.name: Collection name
tb_place.shelf: Shelf
tb_book.name: Book name
tb_book.short_description: Short description
tb_book.description: Description
tb_book.book_size: Size
tb_book.book_year: Year
tb_book.sale: Sale
tb_person.name: Author name
tb_book.city: City
tb_book.book_condition: Condition
tb_person.name: Dedicated to person name
tb_book.edition: Edition
tb_publisher.name: Publisher name
tb_gender.name: Gender
tb_book.ISBN: ISBN
tb_book.pages: Pages

## The script works as follows

The script reads the header of the CSV file to identify the field indexes.
The script reads the rest of the CSV file and extracts the values from each field.
The script inserts the field values into the corresponding tables in the database.

## Requirements

Python 3.8 or higher
MySQL 5.7 or higher

## Instructions for use

Create a MySQL database named "library".
Create the following tables in the database:

``` sql
CREATE TABLE tb_collection (
  collectionid INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE tb_place (
  placeid INT AUTO_INCREMENT PRIMARY KEY,
  shelf VARCHAR(255)
);

CREATE TABLE tb_book (
  bookid INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255),
  short_description VARCHAR(255),
  description TEXT,
  book_size VARCHAR(255),
  book_year INT,
  sale BOOLEAN,
  placeid INT,
  FOREIGN KEY (placeid) REFERENCES tb_place (placeid)
);

CREATE TABLE tb_collection_has_tb_book (
  collectionid INT,
  bookid INT,
  PRIMARY KEY (collectionid, bookid),
  FOREIGN KEY (collectionid) REFERENCES tb_collection (collectionid),
  FOREIGN KEY (bookid) REFERENCES tb_book (bookid)
);

CREATE TABLE tb_book_has_tb_gender (
  gender VARCHAR(255),
  bookid INT,
  PRIMARY KEY (gender, bookid),
  FOREIGN KEY (gender) REFERENCES tb_gender (name),
  FOREIGN KEY (bookid) REFERENCES tb_book (bookid)
);

CREATE TABLE tb_book_has_tb_publisher (
  bookid INT,
  publisherid INT,
  PRIMARY KEY (bookid, publisherid),
  FOREIGN KEY (bookid) REFERENCES tb_book (bookid),
  FOREIGN KEY (publisherid) REFERENCES tb_publisher (publisherid)
);

CREATE TABLE tb_person (
  personid INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255)
);

CREATE TABLE tb_person_has_tb_book (
  personid INT,
  bookid INT,
  author BOOLEAN,
  dedicated_to BOOLEAN,
  dedicated_by BOOLEAN,
  PRIMARY KEY (personid, bookid),
  FOREIGN KEY (personid) REFERENCES tb_person (personid),
  FOREIGN KEY (bookid) REFERENCES tb_book (bookid)
);
```
Copy the script to a directory.
Run the script with the following command:
```python
python script.py
```
The script will create the following file:
- insert_commands.sql: This file contains the SQL commands to insert the data into the database.

## Importing data from SQL file

Now the file "insert_commands.sql" has a list of commands INSERT INTO that you can copy and paste to a MySQL database or run as a SQL file.

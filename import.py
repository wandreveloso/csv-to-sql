import csv

# Function to clean null values
def clean_value(value):
    return value.strip() if value else None

# Function to format a value to SQL command
def _format_sql_value(value):
    return 'NULL' if value is None else f"'{value}'"

# Path of CSV file
csv_file_path = 'novos.csv'

# Reading the header of CSV file
with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)  # Header ignore

# Indexes of header attributes
tb_collection_name_idx = next((i for i, h in enumerate(header) if 'tb_collection.name' in h), None)
tb_place_shelf_idx = next((i for i, h in enumerate(header) if 'tb_place.shelf' in h), None)
tb_book_name_idx = next((i for i, h in enumerate(header) if 'tb_book.name' in h), None)
tb_book_short_description_idx = next((i for i, h in enumerate(header) if 'tb_book.short_description' in h), None)
tb_book_description_idx = next((i for i, h in enumerate(header) if 'tb_book.description' in h), None)
tb_book_size_idx = next((i for i, h in enumerate(header) if 'tb_book.book_size' in h), None)
tb_book_year_idx = next((i for i, h in enumerate(header) if 'tb_book.book_year' in h), None)
tb_book_sale_idx = next((i for i, h in enumerate(header) if 'tb_book.sale' in h), None)
tb_person_name_author_idx = next((i for i, h in enumerate(header) if 'tb_person.name' in h), None)
tb_book_city_idx = next((i for i, h in enumerate(header) if 'tb_book.city' in h), None)
tb_book_condition_idx = next((i for i, h in enumerate(header) if 'tb_book.book_condition' in h), None)
tb_person_name_dedicated_idx = next((i for i, h in enumerate(header) if 'tb_person.name' in h), None)
tb_book_edition_idx = next((i for i, h in enumerate(header) if 'tb_book.edition' in h), None)
tb_publisher_name_idx = next((i for i, h in enumerate(header) if 'tb_publisher.name' in h), None)
tb_gender_name_idx = next((i for i, h in enumerate(header) if 'tb_gender.name' in h), None)
tb_book_isbn_idx = next((i for i, h in enumerate(header) if 'tb_book.ISBN' in h), None)
tb_book_pages_idx = next((i for i, h in enumerate(header) if 'tb_book.pages' in h), None)

# Lists to store unique values
collections = set()
genders = set()
publishers = set()
persons = set()
places = set()

# Generate commands INSERT INTO
with open('insert_commands.sql', 'w', encoding='utf-8') as sql_file:
    # Insertion on intermediate tables
    for collection_name in collections:
        sql_file.write(f"INSERT INTO tb_collection (name) VALUES ('{collection_name}');\n")

    for gender_name in genders:
        sql_file.write(f"INSERT INTO tb_gender (name) VALUES ('{gender_name}');\n")

    for publisher_name in publishers:
        sql_file.write(f"INSERT INTO tb_publisher (name) VALUES ('{publisher_name}');\n")

    for person_name in persons:
        sql_file.write(f"INSERT INTO tb_person (name) VALUES ('{person_name}');\n")

    for place_shelf in places:
        sql_file.write(f"INSERT INTO tb_place (shelf) VALUES ('{place_shelf}');\n")

    # Insertion on main table (tb_book)
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Header ignore again

        for row in reader:
            # Extract the line values
            collection_name = clean_value(row[tb_collection_name_idx])
            place_shelf = clean_value(row[tb_place_shelf_idx])
            book_name = clean_value(row[tb_book_name_idx])
            book_short_description = clean_value(row[tb_book_short_description_idx])
            book_description = clean_value(row[tb_book_description_idx])
            book_size = clean_value(row[tb_book_size_idx])
            book_year = clean_value(row[tb_book_year_idx])
            book_sale = clean_value(row[tb_book_sale_idx])
            person_name_author = clean_value(row[tb_person_name_author_idx])
            book_city = clean_value(row[tb_book_city_idx])
            book_condition = clean_value(row[tb_book_condition_idx])
            person_name_dedicated = clean_value(row[tb_person_name_dedicated_idx])
            book_edition = clean_value(row[tb_book_edition_idx])
            publisher_name = clean_value(row[tb_publisher_name_idx])
            gender_name = clean_value(row[tb_gender_name_idx])
            book_isbn = clean_value(row[tb_book_isbn_idx])
            book_pages = clean_value(row[tb_book_pages_idx])

            # Verify if the table tb_place (shelf) already was inserted
            if place_shelf and place_shelf not in places:
                sql_file.write(f"INSERT INTO tb_place (shelf) VALUES ('{place_shelf}');\n")
                places.add(place_shelf)

            # Generate the command INSERT INTO to main table (tb_book)
            sql_file.write(
                f"INSERT INTO tb_book (name, short_description, description, book_size, book_year, sale, "
                f"city, book_condition, edition, ISBN, pages, placeid) VALUES "
                f"({_format_sql_value(book_name)}, {_format_sql_value(book_short_description)}, "
                f"{_format_sql_value(book_description)}, {_format_sql_value(book_size)}, {_format_sql_value(book_year)}, "
                f"{_format_sql_value(book_sale)}, {_format_sql_value(book_city)}, {_format_sql_value(book_condition)}, "
                f"{_format_sql_value(book_edition)}, {_format_sql_value(book_isbn)}, {_format_sql_value(book_pages)}, "
                f"(SELECT placeid FROM tb_place WHERE shelf = {_format_sql_value(place_shelf)} LIMIT 1));\n"
            )

            # Get the  IDs of intermediate tables
            collection_id_query = f"SELECT collectionid FROM tb_collection WHERE name = '{collection_name}' LIMIT 1"
            book_id_query = f"SELECT bookid FROM tb_book WHERE name = '{book_name}' LIMIT 1"
            person_author_id_query = f"SELECT personid FROM tb_person WHERE name = '{person_name_author}' LIMIT 1"
            person_dedicated_id_query = f"SELECT personid FROM tb_person WHERE name = '{person_name_dedicated}' LIMIT 1"
            gender_id_query = f"SELECT gender FROM tb_gender WHERE name = '{gender_name}' LIMIT 1"
            publisher_id_query = f"SELECT publisherid FROM tb_publisher WHERE name = '{publisher_name}' LIMIT 1"
            place_id_query = f"SELECT placeid FROM tb_place WHERE shelf = '{place_shelf}' LIMIT 1"

            # Generate commands INSERT INTO to intermediate tables
            if collection_name:
                sql_file.write(
                    f"INSERT IGNORE INTO tb_collection_has_tb_book (collectionid, bookid) VALUES (({collection_id_query}), ({book_id_query}));\n"
                )

            if gender_name:
                sql_file.write(
                    f"INSERT IGNORE INTO tb_book_has_tb_gender (gender, bookid) VALUES (({gender_id_query}), ({book_id_query}));\n"
                )


            if publisher_name:
                sql_file.write(
                    f"INSERT IGNORE INTO tb_book_has_tb_publisher (bookid, publisherid) VALUES (({book_id_query}), ({publisher_id_query}));\n"
                )

            if person_name_author:
                sql_file.write(
                    f"INSERT IGNORE INTO tb_person_has_tb_book (personid, bookid, author, dedicated_to, dedicated_by) VALUES (({person_author_id_query}), ({book_id_query}), 1, 0,({person_author_id_query}));\n"
                )

            if person_name_dedicated:
                sql_file.write(
                    f"INSERT IGNORE INTO tb_person_has_tb_book (personid, bookid, author, dedicated_to, dedicated_by) VALUES (({person_dedicated_id_query}), ({book_id_query}), 0, 1, ({person_dedicated_id_query}));\n"
                )

            sql_file.write('\n')


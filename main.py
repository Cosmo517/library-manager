from database_queries import *

# connect to database
con, database_name = create_database_connection()
database_setup(con)
print(database_name)
print(get_all_tables_in_library(con))
insert_into_table(con, 'Mistborn', 1, 'Brandon_Sanderson',
                  750, 10, 'Yes', 'Yes', 'Fantasy', 'Paperback')
print(get_all_rows(con))
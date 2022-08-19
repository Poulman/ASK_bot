import psycopg2

connection = psycopg2.connect(user="pavlo",
                              password="218591",
                              host="127.0.0.1",
                              port="5432",
                              database="accounts")

cursor = connection.cursor()

def create_table():
    create_table_query = '''CREATE TABLE IF NOT EXISTS database
          (CHATID serial PRIMARY KEY,
            username TEXT,
            TOTAL_RAM_USED VARCHAR,
            TOTAL_FILES_NUMBER VARCHAR,
            INFECTED_NUMBER VARCHAR,
            USERFOLDER TEXT,
            DEF_MODE TEXT,
            LANGUAGE TEXT); '''
    cursor.execute(create_table_query)
    connection.commit()

def insert_query(chatid, username, total_ram_used, total_files_number, infected_number, user_folder, def_mode, language):
    insert_query = """ INSERT INTO database (CHATID, username, TOTAL_RAM_USED, TOTAL_FILES_NUMBER, INFECTED_NUMBER, USERFOLDER, DEF_MODE, LANGUAGE) VALUES({}, '{}', {}, {}, {}, '{}', '{}', '{}')""".format(chatid, username, total_ram_used, total_files_number, infected_number, user_folder, def_mode, language)
    cursor.execute(insert_query)
    connection.commit()

def update_by_param(chatid, param, value):
    update_query = """Update database set {} = '{}' where chatid = {}""".format(param, value, chatid)
    cursor.execute(update_query)
    connection.commit()

def update_total_ram_used(total_ram_used, chatid):
    update_query = """Update database set TOTAL_RAM_USED = {} where chatid = {}""".format(total_ram_used, chatid)
    cursor.execute(update_query)
    connection.commit()

def update_total_files_number(total_files_number, chatid):
    update_query = """Update database set TOTAL_FILES_NUMBER = {} where chatid = {}""".format(total_files_number, chatid)
    cursor.execute(update_query)
    connection.commit()

def update_language(language, chatid):
    update_query = """Update database set LANGUAGE = {} where chatid = {}""".format(language, chatid)
    cursor.execute(update_query)
    connection.commit()

cursor.execute("SELECT * from database")
record = cursor.fetchall()


# cursor.execute("DROP TABLE database")
#
#
# for row in record:
#     print("CHATID = ", row[0], )
#     print("username = ", row[1])
#     print("TOTAL_RAM_USED = ", row[2])
#     print("TOTAL_FILES_NUMBER = ", row[3])
#     print("LANGUAGE = ", row[4])

    # print("USERFOLDER  = ", row[5], "\n")


    # cursor.execute("SELECT * from mobile")
    # print("Result ", cursor.fetchall())
    #
    # # Executing a SQL query to delete table
# delete_query = """Delete from database where username = 'ambidexterrrr'"""
# cursor.execute(delete_query)
# connection.commit()
# count = cursor.rowcount
    # print(count, "Record deleted successfully ")
    # # Fetch result
    # cursor.execute("SELECT * from mobile")
    # print("Result ", cursor.fetchall())


# except (Exception, psycopg2.Error) as error:
#     print("Error while connecting to PostgreSQL", error)
# finally:
#     if connection:
#         cursor.close()
#         connection.close()

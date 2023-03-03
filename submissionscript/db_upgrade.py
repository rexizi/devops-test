import sys
import os
import re
import mysql.connector

# set the script params + create DB connection
dir_path = sys.argv[1]

# db_connection = mysql.connector.connect(
#   host=sys.argv[3],
#   user=sys.argv[2],
#   passwd=sys.argv[5],
#   database=sys.argv[4]
# )

# db_cursor = db_connection.cursor(dictionary=True)

def get_files_and_versions():
    list_of_files = sorted(filter(lambda x: os.path.isfile(os.path.join(dir_path, x)), os.listdir(dir_path)))
    versions_and_files = {}

    for file_name in list_of_files:
        version_number = re.findall(r'\d+', file_name)
        if len(version_number) != 0:
            versions_and_files[version_number[0].lstrip('0')] = sys.argv[1] + "/" + file_name

    return versions_and_files

# def get_current_db_version():
#     db_cursor.execute("SELECT max(version) as version FROM versionTable;")
#     result_version = db_cursor.fetchone()
#     print(result_version)


print(get_files_and_versions())

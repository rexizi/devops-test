import sys
import os
import re
import mysql.connector
from typing import Dict
import json

# set the script params + create DB connection
dir_path = sys.argv[1]

db_connection = mysql.connector.connect(
  host=sys.argv[3],
  user=sys.argv[2],
  passwd=sys.argv[5],
  database=sys.argv[4]
)

db_cursor = db_connection.cursor(dictionary=True)

def get_files_and_versions():
    list_of_files = sorted(filter(lambda x: os.path.isfile(os.path.join(dir_path, x)), os.listdir(dir_path)))
    versions_and_files = {}

    for file_name in list_of_files:
        version_number = re.findall(r'\d+', file_name)
        if len(version_number) != 0:
            versions_and_files[version_number[0].lstrip('0')] = sys.argv[1] + file_name

    return versions_and_files

def get_current_db_version():
    db_cursor.execute("SELECT max(version) as version FROM versionTable;")
    result_version = db_cursor.fetchone()
    print(f"Current DB version: {result_version['version']}")
    return result_version['version']

def run_upgrade_scripts(current_scripts: Dict, db_current_version: str):
    for key in current_scripts:
        if int(key) > db_current_version:
            with open(current_scripts[key], 'r') as f:
                print("Scripts to be executed: " + current_scripts[key])
                db_cursor.execute(f.read())
                db_connection.commit()
                print("DB is ready for upgrade!")

    latest_version = int(list(current_scripts)[-1])
    if latest_version <= db_current_version:
        print("No need for upgrade, DB is currently at the latest version!")
    else: 
        print(f"DB will be upgraded to version {latest_version}!")

        db_cursor.execute(f"UPDATE versionTable SET version = {latest_version};")
        db_connection.commit()

        db_cursor.execute("SELECT max(version) as version FROM versionTable;")
        version = db_cursor.fetchone()
        f = open('/scripts/expecteddbstate/versionTable.json', 'w')
        f.write(json.dumps(version))
        f.close()
        print("DB was upgraded successfully!")

run_upgrade_scripts(get_files_and_versions(), get_current_db_version())
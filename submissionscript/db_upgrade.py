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

# get the files containing the script and make a Dict having as keys the version numbers from script names and as values the path for each script 
def get_files_and_versions():
    list_of_files = list(filter(lambda x: os.path.isfile(os.path.join(dir_path, x)), os.listdir(dir_path)))
    versions_and_files = {}

    for file_name in list_of_files:
        if ".sql" in file_name:
            version_number = re.findall(r'\d+', file_name) # used regex to extract the version number at the start of the file
            if len(version_number) != 0:
                versions_and_files[int(version_number[0].lstrip('0'))] = sys.argv[1] + file_name # build the Dict - e.g. {45: '45filename.sql'}

    return dict(sorted(versions_and_files.items())) # return sorted Dict by keys

# get the current DB version
def get_current_db_version():
    db_cursor.execute("SELECT max(version) as version FROM versionTable;")
    result_version = db_cursor.fetchone()
    print(f"Current DB version: {result_version['version']}")
    return result_version['version']

# check if there are any scripts that need to be run and execute them + update the DB version entry with the latest version
def run_upgrade_scripts(current_scripts: Dict, db_current_version: str):
    # get the last key (representing the latest DB version) and 
    latest_version = list(current_scripts)[-1]
    if latest_version <= db_current_version:
        print("No need for upgrade, DB is currently at the latest version!")
    else: 
        # loop through the files dict and compare the keys (versions) to the actual DB version; execute all scripts that match the conditions
        for key in current_scripts:
            if key > db_current_version:
                with open(current_scripts[key], 'r') as f:
                    db_cursor.execute(f.read())
                    db_connection.commit()
                    print("Upgrade script executed: " + current_scripts[key])
        print(f"DB will be upgraded to version {latest_version}!")

        # update the DB version in the table
        db_cursor.execute(f"UPDATE versionTable SET version = {latest_version};")
        db_connection.commit()

        # get the new DB version and update the expecteddbstate file  
        db_cursor.execute("SELECT max(version) as version FROM versionTable;")
        version = db_cursor.fetchone()
        f = open('/scripts/expecteddbstate/versionTable.json', 'w')
        f.write(json.dumps(version))
        f.close()
        print("DB was upgraded successfully!")

run_upgrade_scripts(get_files_and_versions(), get_current_db_version())
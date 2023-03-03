# DevOps Tech Test

### Use Case

- A database upgrade requires the execution of numbered SQL scripts stored in a specified folder, named such as `045.createtable.sql`
  - Sample scripts are provided in the `dbscripts` directory
- The scripts may contain any simple SQL statement(s) to any table of your choice, e.g. `INSERT INTO testTable VALUES("045.createtable.sql");`
- There may be gaps in the SQL file name numbering and there isn't always a . (dot) after the beginning number
- The database upgrade is based on looking up the current version in the database and comparing this number to the numbers in the script names
- The table where the current db version is stored is called `versionTable`, with a single row for the version, called `version`
- If the version number from the db matches the highest number from the scripts then nothing is executed
- All scripts that contain a number higher than the current db version will be executed against the database in numerical order
- In addition, the database version table is updated after the script execution with the executed script's number
- Your script will be executed automatically via a program, and must satisfy these command line input parameters exactly in order to run:
  - `./db-upgrade.your-lang directory-with-sql-scripts username-for-the-db db-host db-name db-password`
  - Example (bash): `./db-upgrade.sh dbscripts myUser myDbServer techTestDB SuperSecretPassword1!`

## Solution

The solution to the above use case is represented mainly by the db_upgrade.py which can be found in the submissionscript dir.
Check the comments in the script for explanations on how it works.
The development of the script was around 3 hours. Extra time was spent for the automation part, adding comments and prints and updating the README.

### Automation

The script is part of crontab and will run automatically on the exec_container at every 5th minute.
You can also manually run the script but after it was run by cron it will print the following message: `No need for upgrade, DB is currently at the latest version!`

## Environment Setup & Testing

### Running the containers

To start the testing environment please run:

```sh
docker-compose up -d
```

This will create two containers called:

- exec_container
- mysql_container

### Testing the script
Commands to be followed:

```sh
docker exec -it exec_container /bin/bash
```

Run the script using

```sh
python3 /submissionscript/db_upgrade.py /scripts/ dev mysql_container devopstt 123456
```

You can then run the test script to check if successful

``` sh
pytest /scripts/db_test.py
```

You can also check the DB to see if all the SQL scripts were executed. Enter the DB password after the below command.
Once you've done that you can execute SQL against the DB e.g. SELECT * FROM someTable . 
``` sh
mysql -u dev -h mysql_container -p devopstt
```

Also check the /scripts/expecteddbstate/versionTable.json file to check if the DB version there was updated too.

Even if the script was ran by cron you can create a new file in the /scripts/ dir and rerun the db_upgrade script. Be advised that in this case the new file should contain a bigger number than the current DB version otherwise it won't be executed. Also, if the file does not contain .sql it won't be executed.

## Database credentials

The database credentials are set in `docker-compose.yml` and are as follows;

```
User: dev
Password: 123456
Database name: devopstt
Database host: mysql_container
```
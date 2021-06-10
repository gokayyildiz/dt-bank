# dt-bank
* Inside the submission folder dt-bank folder carries our all project related codes.
* You should first change directory and go into the dt-bank directory in our submission folder.
* You will see "main.py", "createTables.sql", "triggersAndProcedure.sql", and "inserts.sql" in there.
# Database Initialization
* You should have an active database in MySQL server
* Then, you should go to the MySQL Workbench
* Open a SQL tab and run "use your-database" your-database: the one that you test the program
* After that you can run our queries in the order of createTables.sql > triggersAndProcedure.sql > inserts.sql
* Now, tables and test data is ready
# Database Configuration In main.py
* in main.py at the lines between 11-15, there is database configuration information
* You should set it with your database information in order to succesfully run our program
# Run in Windows
* Open terminal
* Make sure that you are in the /dt-bank/ directory
* run the command "python main.py"
# Run in Mac
* Open terminal
* Make sure that you are in the /dt-bank/ directory
* Run the following commands in the given order:
* export FLASK_APP=main.py
* export FLASK_DEBUG=1
* python3 main.py
# Note:
* While running the code in Mac, if there is an error like: NameError: name '_mysql' is not defined
* You can first run the command: export DYLD_LIBRARY_PATH="/usr/local/mysql/lib:$PATH"
* And run : python3 main.py

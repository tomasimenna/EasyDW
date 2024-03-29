# EasyDW
This is a python application that helps managing small databases using the Windows File Explorer.

With this program, you can select a SQL Server Database and a normal folder from the File Explorer. The program will link them both by using a watchdong that will monitor for every change in the folder, making the changes in the database.

- Whenever we create a csv file inside the targeted folder, it will automatically create a table with that data in the database.
- Whenever we create subfolders inside the targeted folder, it will automatically create databases and schemas.
- Whenever we delete some csv file or folder, it will automatically drop the data from the database.

Currently the program is set to work only with SQL Server but with a simple modification other engines can be added.

----------------------------------------------------------------------------------------------------------------------
Instalation:

a - Clone this repository in your computer:
```
git clone https://github.com/tomasimenna/EasyDW
```
b - Open a cmd, go to the folder where the program got downloaded, and instal the requirements using:
```
pip install -r requirements.txt
```
d - Access to https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16 and download the 'ODBC Driver 17 for SQL Server'. If you will use a different version, you will have to change the connection string in the code.

The connection string appears in the file 'user_interface.py' line 51, in the file 'action_compiler.py' line 31, and in the 'settings_manager.py' line 4. by modifying it, you can use any driver you want, even for databases that are not SQL Server.

----------------------------------------------------------------------------------------------------------------------
Usage:

For using it you will need a SQL Server database. Let's create an example localdb to test it. We are going to create an instance of SQLServer Express LocalDB (from now on, 'the server' by writing in the cmd:
```
sqllocaldb create test_database
```
Now, let's execute the GUI by writing in the cmd:
```
python user_interface.py
```

Insert the server that you want to use, in our case '(localdb)\test_database', and press 'Check & Set'. This will check if is possible to connect to the server.

After that, select the folder that you want to monitor. in our case, we created a folder called 'MyDW' in the Desktop.

Once both parameters are set, press 'Start Monitoring' to start the program.

![image](https://user-images.githubusercontent.com/58273184/186645624-978db37f-bb44-49bc-b1b6-dbf7e064b9b4.png)

Using SSMS18 to check the status of the server, we can check that by starting the program, we created a database called 'basic_settings'. In this database, we can find a table called increasing_tables.

This is because by default, whenever a csv file is replaced in the folder, it replaces the data of the database table. If we want instead to increase the data, we must add the names of the csv files in this database.
Imagine that we want to always increase the content of the file 'pens.csv'. Then we can simply run in SSMS:
```
INSERT INTO dbo.increasing_tables VALUES ('pens')
```
![image](https://user-images.githubusercontent.com/58273184/186648436-540f13c3-4bca-4dfd-a908-e7ff818a1e9a.png)

To create a new database for storing our data, inside the folder 'MyDW' we are going to create a new folder called 'database_1'

We can see that this activity got recorded in the operational logs of the program, who created the database in the server.
![image](https://user-images.githubusercontent.com/58273184/186650997-e0141385-f22f-4033-8bf0-f32f89b64202.png)

Now we are going to create a subfolder in the database and drop some data there. The subfolder will represent a schema, while the data will represent the table.

In the case we just drop data inside the database, it will create the tables in the schema 'dbo'. Let's check it out.

![image](https://user-images.githubusercontent.com/58273184/186653128-391921fb-86f6-4213-bc6f-a53e14d3a37e.png)

In this picture we can see the following:
- We created the subfolder schema_1 --> The schema_1 got created in the database.
- We added the file 'pens.csv' to the folder database_1 --> The table 'pens' got created in the schema 'dbo'.
- We added the file 'folders.csv' in the subfolder 'schema_1' --> The table 'folders' got created in the schema 'schema_1'

Something important to note is that in the log of the program, the table 'folders' appears as 'created' while the table 'pens' appears as appended. This is because earlier we added the table 'pens' to the database of tables to increase. This means that whenever a new file 'folders.csv' will appear in the folder, the table 'schema_1.folders' will be replaced, while whenever a new file 'pens.csv' will appear in the folder, the table 'dbo.pens' will keep the old data and append the new one.

If we want to delete some table, schema, or even database, it is enough with deleting the file or folder that represents it. For example, let's delete the folder 'schema_1'.

![image](https://user-images.githubusercontent.com/58273184/186655877-03adfada-a1ba-4b02-93a3-af6a9ac3d124.png)

----------------------------------------------------------------------------------------------------------------------
Commentaries:
- The program works with multithreadnig to perform all the operations, which means that for example we don't need to wait until a big table gets uploaded to upload the next one. All of them will be uplodaded in paralell.
- There is not limitation to the number of threads, however for SQL server it's recommended not to exceed the 25 threads (in this case, 25 operations at the same time, or upload more than 25 files at a time)

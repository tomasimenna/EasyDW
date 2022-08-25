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

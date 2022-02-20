# CSSWENG-Prime-Properties
*An Inventory Management System for Prime Properties created in Software Engineering (CSSWENG)*

## Use
This project is a tool to help manage the inventory of Prime Properties.

## Pre-requisites
1. MySQL Workbench
  * Tool for designing, modelling, generating, and managing databases.
  * To download: [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)
2. Python / Python3
  * Programming language used.
  * To download in **Windows**: [Python for Windows](https://www.python.org/downloads/windows/)
2. Pip
  * Tool which helps in installing packages written in Python.
  * To download in **Windows**: [Pip for Windows](https://pip.pypa.io/en/stable/installation/)
3. mysql.connector
  * Database driver to connect MySQL Database to the Python program
  * To download in **Windows**: `pip install mysql-connector`
4. pymysql
   * Python MySQL library.
   * To download in **Windows**: `pip install PyMySQL`
5. xlrd
   * Python library for reading data and formatting information from Excel files.
   * To download in **Windows**: `pip install xlrd==1.2.0`
6. pandas.io.sql
   * Python library for data manipulation and analysis.
   * To download in **Windows**: `pip install pandas`
7. PyInstaller
   * Converts Python programs into executables.
   * To download in **Windows**: `pip install pyinstaller`

## Executable file
Open Windows Powershell and run the following command:
```
pyinstaller -F -w main.py --name "Prime Inventory System" --icon "assets/ICON.ico"
```
Go to the created folder "dist" and run the program.

## Members
### SCRUM MASTER
Kyle Lino

### PRODUCT OWNER
Linus Lim

### DESIGNERS
Carissa Bartolome  
Bernice Betito

### DEVELOPERS
Patricia Javier  
Greco Polinga

### QUALITY ASSURANCE
Ysabelle Chen  
Luis Valera

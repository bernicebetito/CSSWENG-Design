import mysql.connector as mysql
import datetime
import os
from mysql.connector import Error 

import pymysql
from pymysql import*
import xlwt
import xlrd
import pandas.io.sql as sql
import openpyxl


class Database():
	def __init__(self):
		# Checks for the instance of the database
		try:
			# ------------------ DB SPECS ------------------ #
			#                     TRICIA                     #
			# db = mysql.connect(
			#   	host = "localhost",
			#   	user = "root",
			#  		passwd = "CSSWENG_Group5",
			#   	database = "prime_properties")
			#
			#                     GRECO                      #
			# db = mysql.connect(
			# 		host = "localhost",
			#		port ='3310', #edited
			#		user = "root",
			#		passwd = "12345", #edited
			#		database = "prime_properties")
			#
			#                    BERNICE                     #
			self.db = mysql.connect(
					host = "localhost",
					port = "3306",
					user = "root",
					passwd = "cssw3nG!",
					database = "prime_properties"
			)
		except Error:
			print("Database Connection Error. Please initialize database.")
			quit()

		# Cursor class instance for executing SQL commands in python
		self.cursor = self.db.cursor()

	# ------------------ DATABASE ACCESS ------------------ #

	def exportToExcel(self):
		# read the data
		df=sql.read_sql('select * from operations', self.db)

		# # print the data for checkking
		# print(df)

		# export the data into the excel sheet
		df.to_excel('operations.xlsx')

		# read the data
		df=sql.read_sql('select * from assets', self.db)

		# # print the data for checking
		# print(df)

		# export the data into the excel sheet
		df.to_excel('assets.xlsx')

	def createDatabase(self, db_name):
		self.cursor.execute("CREATE DATABASE IF NOT EXISTS " + db_name)

	def deleteDatabase(self, db_name):
		self.cursor.execute("DROP DATABASE " + db_name)

	def createTables(self):
		# Users Table: username, password, role
		self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(20) PRIMARY KEY, password VARCHAR(20), role VARCHAR(8))")

		# Assets Table: asset ID, asset name, company, owner, status, unit_loc, price, amount, payment_stat, image, modification date&time
		self.cursor.execute("CREATE TABLE IF NOT EXISTS assets (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), company VARCHAR(255), owner VARCHAR(255), status VARCHAR(255), unit_loc VARCHAR(255), price FLOAT(53,2), amount FLOAT(53,2), payment_stat VARCHAR(255), image LONGBLOB, mod_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")

		# Operations Table: operation ID, receipt no., operation type, username, asset_id, company, ownership, new location, amount, payment_stat, approval status, operation timestamp
		self.cursor.execute("CREATE TABLE IF NOT EXISTS operations (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, receipt_no VARCHAR(255), op_type VARCHAR(255), username VARCHAR(255), authorized_by VARCHAR(255), asset_id INT(11), asset_name VARCHAR(255), recipient VARCHAR(255), company VARCHAR(255), owner VARCHAR(255), unit_loc VARCHAR(255), amount FLOAT(53,2), payment_stat VARCHAR(255), image LONGBLOB, approval_stat VARCHAR(255), op_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

	def deleteTable(self, tb_name):
		self.cursor.execute("DROP TABLE " + tb_name)

	# ------------------ APPLICATION FUNCTIONALITIES ------------------ #
	def createUser(self, username, password, role):
		try:
			query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
			values = (username, password, role)
			self.cursor.execute(query, values)
			self.db.commit()
			return True
		except Error:
			return False

	def getUser(self, username, password):
		try:
			query = "SELECT * FROM users WHERE username = '" + str(username) + "' AND password = '" + str(password) + "'"
			self.cursor.execute(query)
			role = self.cursor.fetchone()
			return(role)
		except Error:
			print("Invalid Credentials. Please Try Again")

	def delUser(self, username):
		try:
			query = "DELETE FROM users WHERE username = '" + str(username) + "'"
			self.cursor.execute(query)
			self.db.commit()
			return True
		except Error:
			return False

	def changePassword(self, username, new_pass):
		try:
			self.cursor.execute("UPDATE users SET password = '" + str(new_pass) + "' WHERE username = '" + str(username) + "'")
			self.db.commit()
			return True
		except Error:
			return False

	def createAsset(self, tb_name, name, company, owner, status, unit_loc, price, amount, payment_stat, image):
		query = "INSERT INTO " + tb_name + " (name, company, owner, status, unit_loc, price, amount, payment_stat, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (name, company, owner, status, unit_loc, price, amount, payment_stat, image)
		self.cursor.execute(query, values)
		self.db.commit()
		print("Successfully Created Asset!")

	def getAsset(self, asset_ID):
		try:
			query = "SELECT * FROM assets WHERE ID = " + str(asset_ID)
			self.cursor.execute(query)
			record = self.cursor.fetchone()
			return (record)
		except Error as error:
			print("Cannot retrieve asset: {}".format(error))

	def delAsset(self, asset_ID):
		try:
			del_query = "DELETE FROM assets "
			ids = "WHERE ID = '"
			for i in asset_ID:
				if ids != "WHERE ID = '":
					ids += " OR ID = '" + str(i) + "'"
				else:
					ids += str(i) + "'"
			del_query += ids

			self.cursor.execute(del_query)
			self.db.commit()
			print("Successfully Deleted Assets!")
		except Error:
			print("Asset Deletion Failed")

	def createReceipt(self, receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat):
		query = "INSERT INTO operations (receipt_no, op_type, username, authorized_by, asset_id, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		values = (receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat)
		self.cursor.execute(query, values)
		self.db.commit()
		print("Successfully Created Receipt!")

	def checkReceiptNo(self, receipt_no):
		query = "SELECT receipt_no FROM operations WHERE receipt_no = '" + str(receipt_no) + "'"
		self.cursor.execute(query)
		check = self.cursor.fetchone()
		if check != None:
			return 1
		else:
			return None

	def viewTable(self, filter, filter_val):
		try:
			if filter == 0: # Users
				if len(filter_val) > 0:
					username = filter_val["username"]
					role = filter_val["role"]

					command = "SELECT username, role, password FROM users"
					filters = " WHERE "
					if len(username) > 0:
						filters += "username = '" + str(username) + "'"
					if len(role) > 0:
						if filters != " WHERE ":
							filters += " AND "
						filters += " role = '" + str(role) + "'"
					if filters != " WHERE ":
						command += filters

					self.cursor.execute(command)
				return self.cursor.fetchall()
			elif filter == 1: # Assets
				name = filter_val["asset_name"]
				company = filter_val["company"]
				owner = filter_val["owner"]
				location = filter_val["location"]
				pay_status = filter_val["pay_status"]
				status = filter_val["status"]

				command = "SELECT id, name, company, owner, unit_loc, price, amount, payment_stat, status, image FROM assets"
				filters = " WHERE "
				if len(name) > 0:
					filters += "name = '" + str(name) + "'"
				if len(company) > 0:
					if filters != " WHERE ":
						filters += " AND "
					filters += "company = '" + str(company) + "'"
				if len(owner) > 0:
					if filters != " WHERE ":
						filters += " AND "
					filters += "owner = '" + str(owner) + "'"
				if len(location) > 0:
					if filters != " WHERE ":
						filters += " AND "
					filters += "unit_loc = '" + str(location) + "'"
				if len(pay_status) > 0:
					if filters != " WHERE ":
						filters += " AND "
					filters += "payment_stat = '" + str(pay_status) + "'"
				if len(status) > 0:
					if filters != " WHERE ":
						filters += " AND "
					filters += "status = '" + str(status) + "'"
				if filters != " WHERE ":
					command += filters

				self.cursor.execute(command)
				return self.cursor.fetchall()
			elif filter == 2: # Operations
				receipt_num = filter_val["receipt_num"]
				name = filter_val["asset_name"]
				owner = filter_val["owner"]
				location = filter_val["location"]
				op_type = filter_val["op_type"]
				in_transit = filter_val["in_transit"]

				command = "SELECT id, receipt_no, op_type, username, authorized_by, asset_id, image, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, approval_stat FROM operations"
				filters = " WHERE "
				if in_transit:
					command = "SELECT operations.id, operations.receipt_no, operations.op_type, operations.username, operations.authorized_by, operations.asset_id, operations.image, operations.asset_name, operations.recipient, operations.company, operations.owner, operations.unit_loc, operations.amount, operations.payment_stat, operations.approval_stat FROM operations INNER JOIN assets ON assets.status LIKE 'In Transit%' AND assets.id = operations.asset_id"
					filters = " AND "
				if len(receipt_num) > 0:
					filters += "operations.receipt_no = '" + str(receipt_num) + "'"
				if len(name) > 0:
					if filters != " WHERE " and filters != " AND ":
						filters += " AND "
					filters += "operations.asset_name = '" + str(name) + "'"
				if len(owner) > 0:
					if filters != " WHERE " and filters != " AND ":
						filters += " AND "
					filters += "operations.owner = '" + str(owner) + "'"
				if len(location) > 0:
					if filters != " WHERE " and filters != " AND ":
						filters += " AND "
					filters += "operations.unit_loc = '" + str(location) + "'"
				if len(op_type) > 0:
					if filters != " WHERE " and filters != " AND ":
						filters += " AND "
					filters += "operations.op_type = '" + str(op_type) + "'"
				if filters != " WHERE " and filters != " AND ":
					command += filters

				self.cursor.execute(command)
				return self.cursor.fetchall()
		except Error:
			print("Failed to retrieve record/s")

	def convertToBinaryData(self, filepath):
		file_exists = os.path.exists(filepath)
		if file_exists is True:
			with open(filepath, 'rb') as file:
				binary_data = file.read()
			return binary_data
		else:
			return False

	def readBLOB(self, asset_ID):		# function for reading/viewing image; can be used in the future, for now just for checking
		query = "SELECT image FROM assets WHERE id = '{0}'"
		self.cursor.execute(query.format(str(asset_ID)))
		result = self.cursor.fetchone()[0]

		curr_path = os.getcwd()
		path = curr_path + "/AssetImages"

		isdir = os.path.isdir(path)

		if isdir is False:
			try:
				os.mkdir(path)
			except OSError:
				print("Creation of the directory %s failed" % path)

		storage_filepath = path + "/asset_{0}.jpeg".format(str(asset_ID))  # saves to AssetImages folder
		with open(storage_filepath, 'wb') as file:
			file.write(result)
			file.close()

		return storage_filepath

	def getAssetfield(self, column, asset_ID):
		query = "SELECT " + column + " FROM assets WHERE id = '" + str(asset_ID) + "'"
		self.cursor.execute(query)
		field = str(self.cursor.fetchone()[0])
		return field

	def setdefaultImage(self, receipt_no, asset_ID):
		query = "UPDATE operations SET operations.image = (SELECT assets.image FROM assets WHERE assets.id = '"+ str(asset_ID) +"') WHERE receipt_no = '" + str(receipt_no) + "'"
		self.cursor.execute(query)
		self.db.commit()

	def delOperation(self, op_id):
		try:
			del_query = "DELETE FROM operations WHERE ID = '" + str(op_id) + "'"
			self.cursor.execute(del_query)
			self.db.commit()
		except Error:
			print("Operation Deletion Failed")

	def approveStat(self, op_id):
		try:
			app_query = "UPDATE operations SET approval_stat = 'Approved' WHERE ID= '" + str(op_id) + "'"
			self.cursor.execute(app_query)
			self.db.commit()
			print("Operation successfully approved!")
		except Error:
			print("Operation Deletion Failed")

	def authorize_asset(self, receipt_no):
		try:
			query = "SELECT * FROM operations WHERE receipt_no = '" + str(receipt_no) + "'"
			self.cursor.execute(query)
			record = self.cursor.fetchone()

			if record[14] != "Approved":
				if record[2] == "Sold":
					query = "UPDATE assets SET status = 'In Transit - Sold', unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"	## record[5] is the asset ID
					self.cursor.execute(query)
					self.db.commit()
					self.approveStat(record[0])	# set approval status to "Approved"

				elif record[2] == "Disposed":
					query = "UPDATE assets SET status = 'In Transit - Disposed', unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"
					self.cursor.execute(query)
					self.db.commit()
					self.approveStat(record[0])

				elif record[2] == "Borrowed":
					query = "UPDATE assets SET status = 'In Transit - Borrowed' , unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"
					self.cursor.execute(query)
					self.db.commit()
					self.approveStat(record[0])

				elif record[2] == "Lent":
					query = "UPDATE assets SET status = 'In Transit - Lent', unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"
					self.cursor.execute(query)
					self.db.commit()
					self.approveStat(record[0])

				elif record[2] == "Update":
					try:
						name = record[6]
						company = record[8]
						owner = record[9]
						unit_loc = record[10]
						amount = record[11]
						payment_stat = record[12]

						#for updatinf asset details
						update_query = "UPDATE assets SET name = '" + str(name) + "', company = '" + str(company) + "', owner = '" + str(owner)\
						+ "', unit_loc = '" + str(unit_loc) + "', amount = '" + str(amount) + "', payment_stat = '" + str(payment_stat)\
						+ "' WHERE id = " + str(record[5])

						self.cursor.execute(update_query)
						self.db.commit()

						#for updating image
						img_query = "UPDATE assets SET assets.image = (SELECT operations.image FROM operations WHERE operations.receipt_no = '"+ str(receipt_no) +"') WHERE ID = '" + str(record[5]) + "'"
						self.cursor.execute(img_query)
						self.db.commit()

						self.approveStat(record[0])
					except Error as error:
						print("Cannot update: {}".format(error))
			else:
				print("The operation you are trying to authorize is already approved")

		except Error as    error:
			print("Failed to authorize: {}".format(error))

	def receiveAsset(self, asset_ID):
		self.cursor.execute("UPDATE assets SET status = REPLACE(status, 'In Transit - ', '') WHERE ID = '" + str(asset_ID) + "' AND status LIKE 'In Transit%'")
		self.db.commit()

	def checkInTransit(self, asset_ID):
		self.cursor.execute("SELECT * FROM assets WHERE ID = '" + str(asset_ID) + "' AND status LIKE 'In Transit%'")
		record = self.cursor.fetchone()
		if record != None:
			print("Receiving asset...")
			self.receiveAsset(asset_ID)
		else:
			print("This asset is not in transit.")


''' Database Initializations'''
# db = Database()
# db.createDatabase("prime_properties")
# db.createTables()

# deleteDatabase("prime_properties")
# deleteTable("users")
# deleteTable("operations")

# Sample accounts for testing purposes
# createUser("admin", "admin1234", "manager")
# createUser("clerk", "clerk1234", "clerk")

# viewTable("users")
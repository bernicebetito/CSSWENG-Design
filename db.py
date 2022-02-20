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
			# db_specs = ["", "CSSWENG_Group5"]

			#                     GRECO                      #
			# db_specs = ["3310", "12345"]

			#                    BERNICE                     #
			db_specs = ["3306", "cssw3nG!"]

			#                     CAR                        #
			# db_specs = ["3310", "12345"]

			self.db = mysql.connect(
				host="localhost",
				port=db_specs[0],
				user="root",
				passwd=db_specs[1],
				database="prime_properties"
			)
		except Error:
			print("Database Connection Error. Please initialize database.")
			quit()

		# Cursor class instance for executing SQL commands in python
		self.cursor = self.db.cursor()

	# ------------------ DATABASE ACCESS ------------------ #

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
		self.cursor.execute("DROP TABLE IF EXISTS " + tb_name)

	def emptyTable(self, tb_name):
		self.cursor.execute("DELETE from " + tb_name + " WHERE id > 0")

	# ------------------ APPLICATION FUNCTIONALITIES ------------------ #
	# USERS
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

	# ASSETS
	def createAsset(self, tb_name, username, name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts):
		try:
			self.cursor.execute("SELECT id FROM assets WHERE name='" + name + "' and owner='" + owner + "' and company='" + company + "' and payment_stat='" + payment_stat + "' and unit_loc='" + unit_loc + "'")
			numrow = self.cursor.fetchone()

			if numrow is not None:
				self.cursor.execute("UPDATE assets SET amount = amount + " + str(amount) + " WHERE id='" + str(numrow[0]) + "'")
				self.db.commit()
			else:
				asset_query = "INSERT INTO " + tb_name + " (name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				asset_values = (name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts)
				self.cursor.execute(asset_query, asset_values)
				self.db.commit()

			self.cursor.execute("SELECT MAX(receipt_no) FROM operations")
			ops_record = self.cursor.fetchone()

			self.cursor.execute("SELECT id FROM assets WHERE name = '" + str(name) + "'")
			asset_record = self.cursor.fetchone()

			if all(ops_record):
				receipt_no = int(ops_record[0]) + 1
			else:
				receipt_no = 1
			op_type = "Create"
			username = username
			asset_id = asset_record[0]
			self.createReceipt(str(receipt_no), op_type, username, None, asset_id, name, None, company, owner, unit_loc, amount, payment_stat, image, None)
			print("Successfully Created Asset!")
		except Error as e:
			print("Failed to create asset: {}".format(e))

	def duplicateAsset(self, tb_name, name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts):
		try:
			asset_query = "INSERT INTO " + tb_name + " (name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			asset_values = (name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts)
			self.cursor.execute(asset_query, asset_values)
			self.db.commit()

			print("Successfully created another instance of an asset.")
		except Error as e:
			print("Failed to duplicate asset: {}".format(e))

	def getAsset(self, asset_ID):
		try:
			query = "SELECT * FROM assets WHERE ID = " + str(asset_ID)
			self.cursor.execute(query)
			record = self.cursor.fetchone()
			return (record)
		except Error as error:
			print("Cannot retrieve asset: {}".format(error))

	def getAssetfield(self, column, asset_ID):
		query = "SELECT " + column + " FROM assets WHERE id = '" + str(asset_ID) + "'"
		self.cursor.execute(query)
		field = str(self.cursor.fetchone()[0])
		return field

	def receiveAsset(self, op_id, asset_ID):
		self.cursor.execute("SELECT asset_name, company, owner, unit_loc, amount, payment_stat FROM operations WHERE id = '" + str(op_id) + "'")
		record = self.cursor.fetchone()

		name = "name = '" + str(record[0]) + "', "
		company = "company = '" + str(record[1]) + "', "
		owner = "owner = '" + str(record[2]) + "', "
		unit_loc = "unit_loc = '" + str(record[3]) + "', "
		amount = "amount = '" + str(record[4]) + "', "
		payment_stat = "payment_stat = '" + str(record[5]) + "', "
		status = "status = REPLACE(status, 'In Transit - ', '')"

		command = name + company + owner + unit_loc + amount + payment_stat + status
		self.cursor.execute("UPDATE assets SET " + command + " WHERE ID = '" + str(asset_ID) + "'")
		self.db.commit()

	def updateAsset(self, update_query):
		try:
			self.cursor.execute(update_query)
			self.db.commit()
		except Error as error:
			print("Update asset failed: {}".format(error))

	def updatePhoto(self, query, args):
		try:
			self.cursor.execute(query,args)
			self.db.commit()
		except Error as error:
			print(error)

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

	def convertToBinaryData(self, filepath):
		file_exists = os.path.exists(filepath)
		if file_exists is True:
			with open(filepath, 'rb') as file:
				binary_data = file.read()
			return binary_data
		else:
			return False

	def readBLOB(self, asset_ID, asset):
		if asset:
			query = "SELECT image FROM assets WHERE id = '{0}' LIMIT 1"
		else:
			query = "SELECT image FROM operations WHERE asset_id = '{0}' LIMIT 1"
		self.cursor.execute(query.format(str(asset_ID)))
		result = self.cursor.fetchone()[0]

		curr_path = os.getcwd()
		path = curr_path + r"\AssetImages"

		isdir = os.path.isdir(path)

		if isdir is False:
			try:
				os.mkdir(path)
			except OSError:
				print("Creation of the directory %s failed" % path)

		storage_filepath = path + r"\asset_{0}.jpeg".format(str(asset_ID))
		with open(storage_filepath, 'wb') as file:
			file.write(result)
			file.close()

		return storage_filepath

	# OPERATIONS
	def createReceipt(self, receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat):
		query = "INSERT INTO operations (receipt_no, op_type, username, authorized_by, asset_id, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat, op_ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		currTime = datetime.datetime.now()
		values = (receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat, currTime)
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
				if record[2] == "Sold" or record[2] == "Disposed" or record[2] == "Borrowed" or record[2] == "Lent":
					query = "UPDATE assets SET status = 'In Transit - " + str(record[2]) + "', unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"
					self.cursor.execute(query)
					self.db.commit()
					self.approveStat(record[0])

				elif record[2] == "Update":
					try:
						name = "UPDATE assets SET name = '" + str(record[6]) + ", "
						company = "company = '" + str(record[8]) + "', "
						owner = "owner = '" + str(record[9]) + "', "
						unit_loc = "unit_loc = '" + str(record[10]) + "', "
						amount = "amount = '" + str(record[11]) + "', "
						payment_stat = "payment_stat = '" + str(record[12]) + "'"
						id_num = " WHERE id = '" + str(record[5]) + "'"

						# Asset Details
						update_query = name + company + owner + unit_loc + amount + payment_stat + id_num

						self.cursor.execute(update_query)
						self.db.commit()

						# Asset Image
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

	def delOperation(self, op_id):
		try:
			del_query = "UPDATE operations SET op_type = CONCAT('Cancelled - ', op_type) WHERE ID = '" + str(op_id) + "'"
			self.cursor.execute(del_query)
			self.db.commit()

			self.cursor.execute("SELECT asset_id FROM operations WHERE id = '" + str(op_id) + "'")
			record = self.cursor.fetchone()

			upd_query = "UPDATE assets SET status = 'Available' WHERE ID = '" + str(record[0]) + "'"
			self.cursor.execute(upd_query)
			self.db.commit()
		except Error:
			print("Operation Deletion Failed")

	# IMPORTING AND EXPORTING
	def importImagesfromFolder(self, filepath, asset_ID):
		path = filepath
		valid_images = [".jpg", ".jpeg", ".gif", ".png", ".tga"]
		asset = "asset_"

		for f in os.listdir(path):
			ext = os.path.splitext(f)[1]
			if ext.lower() in valid_images:
				fname = os.path.splitext(f)[0]
				if fname == (asset + str(int(asset_ID))):
					image = self.convertToBinaryData(os.path.join(path, f))
					return image

		return None

	def importReceipt(self, op_id, receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat):
		query = "INSERT INTO operations (id, receipt_no, op_type, username, authorized_by, asset_id, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat, op_ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		currTime = datetime.datetime.now()
		values = (op_id, receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat, currTime)
		self.cursor.execute(query, values)
		self.db.commit()

	def importAsset(self, tb_name, asset_ID, name, company, owner, status, unit_loc, price, amount, payment_stat, image):
		query = "INSERT INTO " + tb_name + " (id, name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		currTime = datetime.datetime.now()
		values = (asset_ID, name, company, owner, status, unit_loc, price, amount, payment_stat, image, currTime)
		self.cursor.execute(query, values)
		self.db.commit()

	def importToExcel(self, assets_filepath, ops_filepath, photos_dir):
		self.emptyTable("assets")
		self.emptyTable("operations")

		# Import Operations
		wb = xlrd.open_workbook(ops_filepath)
		sheet = wb.sheet_by_index(0)

		for i in range(1, sheet.nrows):
			# Import image from folder of asset images
			img = self.importImagesfromFolder(photos_dir, sheet.cell_value(i, 6))
			if img is None:
				img = self.convertToBinaryData(r"assets\FILLER.jpg")
			# receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approv
			self.importReceipt(sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3),
							   sheet.cell_value(i, 4), sheet.cell_value(i, 5), sheet.cell_value(i, 6),
							   sheet.cell_value(i, 7), sheet.cell_value(i, 8), sheet.cell_value(i, 9),
							   sheet.cell_value(i, 10), sheet.cell_value(i, 11), sheet.cell_value(i, 12),
							   sheet.cell_value(i, 13), img, sheet.cell_value(i, 14))

		# Import Assets
		wb = xlrd.open_workbook(assets_filepath)
		sheet = wb.sheet_by_index(0)
		for i in range(1, sheet.nrows):
			# Import image from folder of asset images
			img = self.importImagesfromFolder(photos_dir, sheet.cell_value(i, 1))
			if img is None:
				img = self.convertToBinaryData(r"assets\FILLER.jpg")
			# assetID, name, company, owner, status, unit_loc, price, amount, payment_stat, image, mod_ts
			self.importAsset("assets", sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3),
						sheet.cell_value(i, 4), sheet.cell_value(i, 5), sheet.cell_value(i, 6),
						sheet.cell_value(i, 7), sheet.cell_value(i, 8), sheet.cell_value(i, 9), img)

	def exportToExcel(self):
		df=sql.read_sql('select id, receipt_no, op_type, username, authorized_by, asset_id, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, approval_stat, op_ts from operations', self.db)
		df.to_excel('operations.xlsx')

		df=sql.read_sql('select id, name, company, owner, status, unit_loc, price, amount, payment_stat, mod_ts from assets', self.db)
		df.to_excel('assets.xlsx')

	# GENERAL
	def viewTable(self, filter, filter_val):
		try:
			if filter == 0:  # Users
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
			elif filter == 1:  # Assets
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
			elif filter == 2:  # Operations
				receipt_num = filter_val["receipt_num"]
				name = filter_val["asset_name"]
				owner = filter_val["owner"]
				location = filter_val["location"]
				op_type = filter_val["op_type"]
				in_transit = filter_val["in_transit"]

				command = "SELECT id, receipt_no, op_type, username, authorized_by, asset_id, image, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, approval_stat FROM operations"
				filters = " WHERE "
				if in_transit:
					command = "SELECT opsA.id, opsA.receipt_no, opsA.op_type, opsA.username, opsA.authorized_by, opsA.asset_id, opsA.image, opsA.asset_name, opsA.recipient, opsA.company, opsA.owner, opsA.unit_loc, opsA.amount, opsA.payment_stat, opsA.approval_stat FROM operations as opsA INNER JOIN (SELECT max(id) as max_id, receipt_no, op_type, username, authorized_by, asset_id, image, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, approval_stat FROM operations GROUP BY asset_id ) opsB ON opsA.id = max_id INNER JOIN assets ON assets.status LIKE 'In Transit%' AND assets.id = opsA.asset_id AND opsA.op_type IN ('Move', 'Sold', 'Disposed', 'Borrowed', 'Lent')"
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
					if op_type == "Cancelled":
						filters += "operations.op_type LIKE '" + str(op_type) + "%'"
					else:
						filters += "operations.op_type = '" + str(op_type) + "'"
				if in_transit:
					filters = filters.replace("operations", "opsA")
				if filters != " WHERE " and filters != " AND ":
					command += filters

				self.cursor.execute(command)
				return self.cursor.fetchall()
		except Error:
			print("Failed to retrieve record/s")

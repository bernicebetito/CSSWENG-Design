import mysql.connector as mysql
import datetime
import os
from mysql.connector import Error 

import pymysql
from pymysql import*
import xlwt
import xlrd
import pandas.io.sql as sql

# Checks for the instance of the database
try:
	## Connecting to the Database
	# db = mysql.connect(		# Tricia Database Specs
	#   	host = "localhost",
	#   	user = "root",
	#  	passwd = "CSSWENG_Group5",
	#   	database = "prime_properties")

	db = mysql.connect(		# Greco Database Specs
		host = "localhost",
		port='3310', #edited
		user = "root",
		passwd = "12345", #edited
		database = "prime_properties")
except Error:
	print("Database Connection Error. Please initialize database.")
	quit()

# Cursor class instance for executing SQL commands in python
cursor = db.cursor()

### DATABASE ACCESS

def exportToExcel():
	# connect the mysql with the python
	con=connect(		
		host = "localhost",
		port=3310, #edited
		user = "root",
		passwd = "12345", #edited
		database = "prime_properties")
	# read the data
	df=sql.read_sql('select * from operations',con)
	
	# # print the data for checkking
	# print(df)

	# export the data into the excel sheet
	df.to_excel('operations.xlsx')

	# read the data
	df=sql.read_sql('select * from assets',con)
	
	# # print the data for checking
	# print(df)

	# export the data into the excel sheet
	df.to_excel('assets.xlsx')



def createDatabase(db_name):
	cursor.execute("CREATE DATABASE IF NOT EXISTS " + db_name)

def deleteDatabase(db_name):
	cursor.execute("DROP DATABASE " + db_name)

def createTables():
	# Users Table: username, password, role
	cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(20) PRIMARY KEY, password VARCHAR(20), role VARCHAR(8))")

	# Assets Table: asset ID, asset name, company, owner, status, unit_loc, price, amount, payment_stat, image, modification date&time
	cursor.execute("CREATE TABLE IF NOT EXISTS assets (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), company VARCHAR(255), owner VARCHAR(255), status VARCHAR(255), unit_loc VARCHAR(255), price FLOAT(53,2), amount FLOAT(53,2), payment_stat VARCHAR(255), image LONGBLOB, mod_ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")

	# Operations Table: operation ID, receipt no., operation type, username, asset_id, company, ownership, new location, amount, payment_stat, approval status, operation timestamp
	cursor.execute("CREATE TABLE IF NOT EXISTS operations (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, receipt_no VARCHAR(255), op_type VARCHAR(255), username VARCHAR(255), authorized_by VARCHAR(255), asset_id INT(11), asset_name VARCHAR(255), recipient VARCHAR(255), company VARCHAR(255), owner VARCHAR(255), unit_loc VARCHAR(255), amount FLOAT(53,2), payment_stat VARCHAR(255), image LONGBLOB, approval_stat VARCHAR(255), op_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

def deleteTable(tb_name):
	cursor.execute("DROP TABLE " + tb_name)

### APPLICATION FUNCTIONALITIES

def createUser(username, password, role):
	try:
		query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
		values = (username, password, role)
		cursor.execute(query, values)
		db.commit()
		print("Successfully Created a User!")
	except Error:
		print("User Creation Failed")

def getUser(username, password):
	try:
		query = "SELECT * FROM users WHERE username = '" + str(username) + "' AND password = '" + str(password) + "'"
		cursor.execute(query)
		role = cursor.fetchone()
		return(role)
	except Error:
		print("Invalid Credentials. Please Try Again")

def delUser(username):
	try:
		query = "DELETE FROM users WHERE username = '" + str(username) + "'"
		cursor.execute(query)
		db.commit()
		print("Successfully Deleted User!")
	except Error:
		print("User Deletion Failed")

def createAsset(tb_name, name, company, owner, status, unit_loc, price, amount, payment_stat, image):
	query = "INSERT INTO " + tb_name + " (name, company, owner, status, unit_loc, price, amount, payment_stat, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	values = (name, company, owner, status, unit_loc, price, amount, payment_stat, image)
	cursor.execute(query, values)
	db.commit()
	print("Successfully Created Asset!")

def createReceipt(receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat):
	query = "INSERT INTO operations (receipt_no, op_type, username, authorized_by, asset_id, asset_name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	values = (receipt_no, op_type, username, auth, asset_id, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval_stat)
	cursor.execute(query, values)
	db.commit()
	print("Successfully Created Receipt!")

def checkReceiptNo(receipt_no):
	query = "SELECT receipt_no FROM operations WHERE receipt_no = '" + str(receipt_no) + "'"
	cursor.execute(query) 
	check = cursor.fetchone()
	if check != None:
		return 1
	else:
		return None	

def getAsset(asset_ID):
	try:
		query = "SELECT * FROM assets WHERE ID = " + str(asset_ID)
		cursor.execute(query)
		record = cursor.fetchone()
		return (record)
	except Error as    error:
		print("Cannot retrieve asset: {}".format(error))

def viewTable(filter, filter_val):
	try:
		if filter == 0:
			cursor.execute("SELECT username, role FROM users")
			records = cursor.fetchall()

			for record in records:
				print(record)
		elif filter == 1:
			cursor.execute("SELECT image, name, company, owner, unit_loc, price, payment_stat, status FROM assets")
			records = cursor.fetchall()

			for record in records:
				print(record)
		elif filter == 2:
			cursor.execute("SELECT image, name, company, owner, unit_loc, price, payment_stat FROM assets WHERE name = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		elif filter == 3:
			cursor.execute(
				"SELECT image, name, company, owner, unit_loc, price, payment_stat FROM assets WHERE unit_loc = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		elif filter == 4:
			cursor.execute("SELECT image, name, company, owner, unit_loc, price, payment_stat FROM assets WHERE owner = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		elif filter == 5:
			cursor.execute("SELECT image, name, company, owner, unit_loc, price, payment_stat FROM assets WHERE status = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		else:
			print("Unrecognized Filter")
	except Error:
		print("Failed to retrieve record/s")

def viewOperations(filter, filter_val):
	try:
		# View all
		if filter == 1:
			cursor.execute("SELECT image, asset_name, company, owner, unit_loc, payment_stat, amount FROM operations")
			records = cursor.fetchall()

			for record in records:
				print(record)	

		# Filter by Name
		elif filter == 2:
			cursor.execute("SELECT image, asset_name, company, owner, unit_loc, payment_stat, amount FROM operations WHERE asset_name = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		# Filter by Location		
		elif filter == 3:
			cursor.execute(
				"SELECT image, asset_name, company, owner, unit_loc, payment_stat, amount FROM operations WHERE unit_loc = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		# Filter by Owner
		elif filter == 4:
			cursor.execute("SELECT image, asset_name, company, owner, unit_loc, payment_stat, amount FROM operations WHERE owner = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		# Filter by Approval Status		
		elif filter == 5:
			cursor.execute("SELECT image, asset_name, company, owner, unit_loc, payment_stat, amount FROM operations WHERE approval_stat = '" + str(filter_val) + "'")
			records = cursor.fetchall()

			for record in records:
				print(record)
		else:
			print("Unrecognized Filter")

	except Error as error:
		print(error)	

def filterOperations(filter_type):
	print("\nHISTORY TABLE\n")
	if filter_type == 1:
		viewOperations(1,"None")
	elif filter_type == 2:
		filter_val = input("Input Asset Name: ")
		viewOperations(2, filter_val)
	elif filter_type == 3:
		filter_val = input("Input Location: ")
		viewOperations(3, filter_val)
	elif filter_type == 4:
		filter_val = input("Input Owner: ")
		viewOperations(4, filter_val)
	elif filter_type == 5:
		print("[1] Approved\n[2] Unapproved")
		filter_val = int(input("Choose Approval Status: "))
		if filter_val == 1:
			viewOperations(5, "Approved")
		elif filter_val == 2:
			viewOperations(5, "Unapproved")
		else:
			print("Invalid Input")
	elif filter_type == 6:
		filter_val = input("Input Receipt No.: ")
		if checkReceiptNo(filter_val) != None:
			viewOperations(6, filter_val)
		else:
			print("Non-existing receipt number")
	else:
		print("Invalid Input")

def filterAsset(filter_type):
	print("\nASSETS TABLE\n")
	if filter_type == 1:
		viewTable(1,"None")
	elif filter_type == 2:
		filter_val = input("Input Asset Name: ")
		viewTable(2, filter_val)
	elif filter_type == 3:
		filter_val = input("Input Location: ")
		viewTable(3, filter_val)
	elif filter_type == 4:
		filter_val = input("Input Owner: ")
		viewTable(4, filter_val)
	elif filter_type == 5:
		print("\n[1] Available\n[2] Sold\n[3] Disposed\n[4] Borrowed\n[5] Lent")
		filter_val = int(input("Choose Status: "))
		if filter_val == 1:
			viewTable(5, "Available")
		elif filter_val == 2:
			viewTable(5, "Sold")
		elif filter_val == 3:
			viewTable(5, "Disposed")
		elif filter_val == 4:
			viewTable(5, "Borrowed")
		elif filter_val == 5:
			viewTable(5, "Lent")
		else:
			print("Invalid Input")
	elif filter_type == 6:
		filter_val = input("Input Receipt No.: ")
		if checkReceiptNo(filter_val) != None:
			viewOperations(6, filter_val)
		else:
			print("Non-existing receipt number")
	else:
		print("Invalid Input")

def filterUser():
	print("\nUSERS TABLE\n")
	viewTable(0,"None")

def delAsset(asset_ID):
	try:
		del_query = "DELETE FROM assets WHERE ID = '" + asset_ID + "'"
		cursor.execute(del_query)
		db.commit()
		print("Successfully Deleted Asset!")
	except Error:
		print("Asset Deletion Failed")

def convertToBinaryData(filepath):
	file_exists = os.path.exists(filepath)
	if file_exists is True:
		with open(filepath, 'rb') as file:
			binary_data = file.read()
		return binary_data
	else:
		return False

def readBLOB(asset_ID):		# function for reading/viewing image; can be used in the future, for now just for checking
	query = "SELECT image FROM assets WHERE id = '{0}'"
	cursor.execute(query.format(str(asset_ID)))
	result = cursor.fetchone()[0]

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

def inputAsset():
	name = input("Asset Name: ")
	company = input("Company: ")
	owner = input("Ownership: ")
	status = "Available"  # default

	unit_loc = input("Unit Location: ")

	# for checking if input is float/decimal
	while True:
		try:
			price = float(input("Price: "))
			if isinstance(price, float):
				break
		except:
			print("Invalid format for price")
			pass

	while True:
		try:
			amount = float(input("Amount: "))
			if isinstance(amount, float):
				break
		except:
			print("Invalid format for amount")
			pass

	while 1:
		print("Payment Status (Choose among the options)")
		print("[1] Paid \n[2] Unpaid \nOption: ")
		pstat_option = int(input())

		if pstat_option == 1:
			payment_stat = "Paid"
			break
		elif pstat_option == 2:
			payment_stat = "Unpaid"
			break
		else:
			print("Invalid option")

	while 1:
		print("Upload image of asset")
		temp_image = input("Enter filepath of image (example: C:\\Users\\Desktop\\image.jpg): ")
		if convertToBinaryData(temp_image) != False:
			image = convertToBinaryData(temp_image)
			break
		else:
			print("Image not found. Please try again")

	try:
		createAsset("assets", name, company, owner, status, unit_loc, price, amount, payment_stat, image)
	except Error as error:
		print("Failed to create asset: {}".format(error))

def getAssetfield(column, asset_ID):
	query = "SELECT " + column + " FROM assets WHERE id = '" + str(asset_ID) + "'"
	cursor.execute(query) 
	field = str(cursor.fetchone()[0])
	return field

def setdefaultImage(receipt_no, asset_ID):
	query = "UPDATE operations SET operations.image = (SELECT assets.image FROM assets WHERE assets.id = '"+ str(asset_ID) +"') WHERE receipt_no = '" + str(receipt_no) + "'"
	cursor.execute(query)
	db.commit()

def delOperation(op_id):
	try:
		del_query = "DELETE FROM operations WHERE ID = '" + str(op_id) + "'"
		cursor.execute(del_query)
		db.commit()
	except Error:
		print("Operation Deletion Failed")

def approveStat(op_id):
	try:
		app_query = "UPDATE operations SET approval_stat = 'Approved' WHERE ID= '" + str(op_id) + "'"
		cursor.execute(app_query)
		db.commit()
		print("Operation successfully approved!")
	except Error:
		print("Operation Deletion Failed")

def authorize_asset(receipt_no):
	try:
		query = "SELECT * FROM operations WHERE receipt_no = '" + str(receipt_no) + "'"
		cursor.execute(query)
		record = cursor.fetchone()
		
		if record[14] != "Approved":
			if record[2] == "Sold":
				query = "UPDATE assets SET status = 'In Transit - Sold', unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"	## record[5] is the asset ID
				cursor.execute(query)
				db.commit()
				approveStat(record[0])	# set approval status to "Approved"

			elif record[2] == "Disposed":
				query = "UPDATE assets SET status = 'In Transit - Disposed', unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"
				cursor.execute(query)
				db.commit()
				approveStat(record[0])	
			
			elif record[2] == "Borrowed":
				query = "UPDATE assets SET status = 'In Transit - Borrowed' , unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"
				cursor.execute(query)
				db.commit()
				approveStat(record[0])	

			elif record[2] == "Lent":
				query = "UPDATE assets SET status = 'In Transit - Lent', unit_loc = '" + str(record[10]) + "' WHERE ID = '" + str(record[5]) + "'"
				cursor.execute(query)
				db.commit()
				approveStat(record[0])	

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

					cursor.execute(update_query)
					db.commit()

					#for updating image
					img_query = "UPDATE assets SET assets.image = (SELECT operations.image FROM operations WHERE operations.receipt_no = '"+ str(receipt_no) +"') WHERE ID = '" + str(record[5]) + "'"
					cursor.execute(img_query)
					db.commit()

					approveStat(record[0])	
				except Error as error:
					print("Cannot update: {}".format(error))
		else:
			print("The operation you are trying to authorize is already approved")		

	except Error as    error:
		print("Failed to authorize: {}".format(error))

def getInTransit():
	cursor.execute("SELECT id, name, company, owner, unit_loc, price, payment_stat, status FROM assets WHERE status LIKE 'In Transit%'")
	records = cursor.fetchall()
	if records != None:
		for record in records:
			print(record)
	else:
		print("No assets in transit")

def receiveAsset(asset_ID):
	cursor.execute("SELECT status FROM assets WHERE ID = '" + str(asset_ID) + "'")
	record = cursor.fetchone()
	if record[0] == "In Transit - Sold":
		cursor.execute("UPDATE assets SET status = 'Sold' WHERE ID = '" + str(asset_ID) + "' AND status LIKE 'In Transit%'")
		db.commit()
	elif record[0] == "In Transit - Disposed":
		cursor.execute("UPDATE assets SET status = 'Disposed' WHERE ID = '" + str(asset_ID) + "' AND status LIKE 'In Transit%'")
		db.commit()
	elif record[0] == "In Transit - Borrowed":
		cursor.execute("UPDATE assets SET status = 'Borrowed' WHERE ID = '" + str(asset_ID) + "' AND status LIKE 'In Transit%'")
		db.commit()
	elif record[0] == "In Transit - Lent":
		cursor.execute("UPDATE assets SET status = 'Lent' WHERE ID = '" + str(asset_ID) + "' AND status LIKE 'In Transit%'")
		db.commit()

	cursor.execute("SELECT id, name, company, owner, unit_loc, price, payment_stat, status FROM assets WHERE ID = '" + str(asset_ID) + "'")
	record = cursor.fetchone()
	print("Updated Status: " + str(record))

def checkInTransit(asset_ID):
	cursor.execute("SELECT * FROM assets WHERE ID = '" + str(asset_ID) + "' AND status LIKE 'In Transit%'")
	record = cursor.fetchone()
	if record != None:
		print("Receiving asset...")
		receiveAsset(asset_ID)
	else:
		print("This asset is not in transit.")

def changePassword(username,new_pass):
	try:
		cursor.execute("UPDATE users SET password = '" + str(new_pass) + "' WHERE username = '" + str(username) + "'")
		db.commit()
		print("Successfully changed password!")
	except Error:
		print("Password change unsuccessful")

''' Database Initializations'''
createDatabase("prime_properties")
createTables()

#deleteDatabase("prime_properties")
#deleteTable("users")
#deleteTable("operations")

## Sample accounts for testing purposes
#createUser("admin", "admin1234", "manager")
#createUser("clerk", "clerk1234", "clerk")

#viewTable("users")

while True:
	user = input("Username: ")
	passw = input("Password: ")

	credentials = getUser(user, passw)

	# If account exists
	if credentials != None:

		# get the role
		role = credentials[2]

		# Every user session
		session = True

		while session:

			if role == "manager":
				# Manager Nav Page
				print("\n[1] Create Asset\n[2] Create User\n[3] Find\n[4] History\n[5] Update\n[6] Delete\n[7] Receive\n[8] Change Password\n[9] Export Database to Excel\n[10] Logout")
				command = int(input("Choose Action: "))

				if command == 1:
					print("\nCREATE ASSET\n")
					# Create Asset Page
					inputAsset()

				elif command == 2:
					# Create Users Page
					print("\nCREATE A USER\n")
					username = input("Username (Max 20 characters): ")
					password = input("Password (Max 20 characters): ")
					print("[1] Manager\t[2] Inventory Clerk")
					user_role = int(input("Choose User Role: "))

					if user_role == 1:
						createUser(username, password, "manager")
					elif user_role == 2:
						createUser(username, password, "clerk")
					else:
						print("\nInvalid Input\n")

				elif command == 3:
					print("\n[1] Assets\n[2] Users")
					view = int(input("What to view? "))

					if view == 1:
						while 1:
							print("\nVIEW ASSETS\n")
							print("[1] View All\n[2] Filter Asset Name\n[3] Filter Location\n[4] Filter Owner\n[5] Filter Status\n[6] Receipt No.\n[0] Back")
							filter_type = int(input("Search by: "))
							if filter_type >=1 and filter_type <= 6:
								filterAsset(filter_type)
							elif filter_type == 0:
								break
							else:
								print("Invalid input")	
					elif view == 2:
						filterUser()
					else:
						print("\nInvalid Input\n")

				elif command == 4:
					while 1:
						print("\nVIEW HISTORY\n")
						print("[1] View All\n[2] Filter Asset Name\n[3] Filter Location\n[4] Filter Owner\n[5] Filter Status\n[6] Receipt No.\n[0] Back")
						filter_type = int(input("Search by: "))
						if filter_type >=1 and filter_type <= 6:
							filterOperations(filter_type)
						elif filter_type == 0:
							break
						else:
							print("Invalid input")	

				elif command == 5:
					while 1:
						print("\nUPDATE ASSET\n")
						print("[1] Perform Operation\n[2] Authorize\n[3] Back")
						option = int(input("Option: "))

						# Perform Operation
						if option == 1:
							print("[1] Sold\n[2] Disposed\n[3] Borrowed\n[4] Lent\n[5] Update")
							op_type = int(input("Choose Operation Type: "))

							asset_ID = input("Enter Asset ID: ")

							if getAsset(asset_ID) != None:

								# Get username of user
								username = credentials[0]

								## Get current details of editable fields in asset / set to default
								image = getAssetfield("image", asset_ID)
								name = getAssetfield("name", asset_ID)
								company = getAssetfield("company", asset_ID)
								owner = getAssetfield("owner", asset_ID)
								status = getAssetfield("status", asset_ID)
								unit_loc = getAssetfield("unit_loc", asset_ID)
								price = getAssetfield("price", asset_ID)
								amount = getAssetfield("amount", asset_ID)
								payment_stat = getAssetfield("payment_stat", asset_ID)

								recipient = ""

								if op_type == 1:
									# since option chosen is sold, set status to sold
									status = "In Transit - Sold"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Sold"
												unit_loc = input("Location: ")
												owner = input("Owner: ")
												recipient = input("Recipient: ")
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = ""

												# since this is a manager account, ask for approval stat
												while 1:
													print("\n[1] Yes\t[2] No")
													app = int(input("Approve this operation? "))

													if app == 1:
														approval = "Approved"
														break
													elif app == 2:
														approval = "Unapproved"
														break
													else:
														print("Invalid Input")
												try:
													if approval == "Approved":
														update_query = "UPDATE assets SET status = '" + status + "', unit_loc = '" + unit_loc +  "', owner = '" + owner + "' WHERE id = " + str(asset_ID)
														cursor.execute(update_query)
														db.commit()

													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID) #since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 2:
									# since option chosen is disposed, set status to sold
									status = "In Transit - Disposed"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Disposed"
												unit_loc = input("Location: ")
												recipient = input("Recipient: ")
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = ""

												# since this is a manager account, ask for approval stat
												while 1:
													print("\n[1] Yes\t[2] No")
													app = int(input("Approve this operation? "))

													if app == 1:
														approval = "Approved"
														break
													elif app == 2:
														approval = "Unapproved"
														break
													else:
														print("Invalid Input")
												try:
													if approval == "Approved":
														update_query = "UPDATE assets SET status = '" + status + "', unit_loc = '" + unit_loc + "' WHERE id = " + str(asset_ID)
														cursor.execute(update_query)
														db.commit()
													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID) #since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 3:
									# since option chosen is borrowed, set status to sold
									status = "In Transit - Borrowed"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Borrowed"
												unit_loc = input("Location: ")
												recipient = input("Recipient: ")
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = ""

												# since this is a manager account, ask for approval stat
												while 1:
													print("\n[1] Yes\t[2] No")
													app = int(input("Approve this operation? "))

													if app == 1:
														approval = "Approved"
														break
													elif app == 2:
														approval = "Unapproved"
														break
													else:
														print("Invalid Input")
												try:
													if approval == "Approved":
														update_query = "UPDATE assets SET status = '" + status + "', unit_loc = '" + unit_loc + "' WHERE id = " + str(asset_ID)
														cursor.execute(update_query)
														db.commit()
													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID)	#since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 4:
									# since option chosen is lent, set status to sold
									status = "In Transit - Lent"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Lent"
												unit_loc = input("Location: ")
												recipient = input("Recipient: ")
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = ""

												# since this is a manager account, ask for approval stat
												while 1:
													print("\n[1] Yes\t[2] No")
													app = int(input("Approve this operation? "))

													if app == 1:
														approval = "Approved"
														break
													elif app == 2:
														approval = "Unapproved"
														break
													else:
														print("Invalid Input")
												try:
													if approval == "Approved":
														update_query = "UPDATE assets SET status = '" + status + "', unit_loc = '" + unit_loc + "' WHERE id = " + str(asset_ID)
														cursor.execute(update_query)
														db.commit()
													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID)	#since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 5:
									check_changes = False 	#set changes made to false
									updated_image = False    ##set to false
									
									while 1:
										# update other info
										print("\nChoose fields to update")
										print("[1] Asset Name \n[2] Company \n[3] Ownership \n[4] Unit Location\n[5] Amount\n[6] Payment Status\n[7] Image\n[8] Save changes\n[9] Back\nOption (Save changes when done): ")
										update_cmd = int(input())

										# update asset name
										if update_cmd == 1:
											name = input("Edit Asset Name: ")
											check_changes = True
										# update company
										elif update_cmd == 2:
											company = input("Edit Company: ")
											check_changes = True
										# update ownership
										elif update_cmd == 3:
											owner = input("Edit Ownership: ")
											check_changes = True
										# update unit location
										elif update_cmd == 4:
											unit_loc = input("Update Unit Location: ")
											check_changes = True
										# update amount
										elif update_cmd == 5:
											while True:
												try:
													holder = float(input("Update Amount: "))
													if isinstance(holder, float):
														amount = holder
														check_changes = True
														break
												except:
													print("Invalid format for amount")
													pass
										# update payment status
										elif update_cmd == 6:
											while 1:
												print("Payment Status (Choose among the options)")
												print("[1] Paid \n[2] Unpaid \nOption: ")
												pstat_option = int(input())

												if pstat_option == 1:
													payment_stat = "Paid"
													check_changes = True
													break

												elif pstat_option == 2:
													payment_stat = "Unpaid"
													check_changes = True
													break

												else:
													print("Invalid option")
										elif update_cmd == 7:
											print("Upload image of asset")
											holder = input("Enter filepath of image (example: C:\\Users\\Desktop\\image.jpg): ")
											if convertToBinaryData(holder) != False:
												image = convertToBinaryData(holder)
												updated_image = True
												check_changes = True
											else:
												print("Image not found. Please try again")

										elif update_cmd == 8:
											if check_changes == True: 
												try:
													update_query = "UPDATE assets SET name = '" + name + "', company = '" + company + "', owner = '" + owner\
													 + "', unit_loc = '" + unit_loc + "', price = '" + str(price) + "', amount = '" + str(amount) + "', payment_stat = '" + payment_stat\
													 + "' WHERE id = " + str(asset_ID)

													# generate receipt
													print("\nRECEIPT PAGE\n")
													while 1:
														receipt_no = input("Enter receipt number: ")
														if checkReceiptNo(receipt_no) == None:
															op_type = "Update"
															recipient = "None"
															username = str(credentials[0])
															auth = input("Authorized By: ")
															approval = ""

															# since this is a manager account, ask for approval stat
															while 1:
																print("\n[1] Yes\t[2] No")
																app = int(input("Approve this operation? "))

																if app == 1:
																	approval = "Approved"
																	break
																elif app == 2:
																	approval = "Unapproved"
																	break
																else:
																	print("Invalid Input")
															try:
																# Commit updated details of asset to database (not including image update)
																if approval == "Approved":
																	cursor.execute(update_query) # only call update_query if operation is approved
																	db.commit()

																	if updated_image == True:	#if image was also updated
																		query =  "UPDATE assets SET image = %s WHERE id = %s" 
																		args = (image, str(asset_ID))

																		try:
																			cursor.execute(query,args)
																			db.commit()
																		except Error as error:
																				print(error)

																createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
																if updated_image == False:
																	setdefaultImage(receipt_no, asset_ID)

															except Error as error:
																print(error)
															break
														else:
															print("Receipt number already exists.")
													break					
												except Error as error:
													print(error)
											else:
												print("No changes were made.")
											
										elif update_cmd == 9:
											break
										else:
											print("Invalid Input")
								else:
									print("Invalid Input")
							else:
								print("Asset ID not found")
						# Authorize Asset
						elif option == 2:
							print("\nAUTHORIZE\n")
							receipt_no = input("Enter Receipt number: ")

							query = "SELECT receipt_no FROM operations WHERE receipt_no = '" + receipt_no + "'"
							cursor.execute(query)
							op_record = str(cursor.fetchone()[0])

							if receipt_no != None:
								print("[1] Yes\t[2] No")
								proceed = int(input("Proceed to authorize operation with receipt number: " + op_record + " ? "))

								if proceed == 1:
									authorize_asset(receipt_no)
								elif proceed == 2:
									print("Cancelled authorization")
								else:
									print("Invalid Input")
							else:
								print("\nNonexistent Operation\n")

						elif option == 3:
							break
						else:
							print("Invalid Input")

				elif command == 6:
					print("\nDELETE\n")
					print("[1] User\n[2] Asset")
					delete = int(input("What to delete? "))

					if delete == 1:
						print("\nDELETE USER\n")
						user_del = input("Enter Username of Account: ")
						# Check if existing username
						query = "SELECT * FROM users WHERE username = '" + str(user_del) + "'"
						cursor.execute(query)
						user_record = cursor.fetchone()

						if user_record != None:

							# checks if self
							if user_record[0] == credentials[0]:
								print("Cannot delete logged-in account.")

							else:
								print("[1] Yes\t[2] No")
								proceed = int(input("Proceed to delete account: " + str(user_record) + "? "))

								if proceed == 1:
									delUser(user_del)
								elif proceed == 2:
									print("Cancelled user deletion")
								else:
									print("Invalid Input")

						else:
							print("\nNonexistent Account\n")

					elif delete == 2:
						print("\nDELETE ASSET\n")
						asset_ID = input("Enter Asset ID: ")
						asset_del = getAsset(asset_ID)

						if asset_del != None:
							print("[1] Yes\t[2] No")
							print("Asset: " + str(asset_del))
							proceed = int(input("Proceed to delete this asset? "))

							if proceed == 1:
								delAsset(asset_ID)
							elif proceed == 2:
								print("Cancelled user deletion")
							else:
								print("Invalid Input")

						else:
							print("Asset ID not found")

					else:
						print("Invalid Input")

				elif command == 7:
					getInTransit()
					receive = int(input("Enter asset ID to be received: "))
					checkInTransit(receive)

				elif command == 8:
					print("\nCHANGE PASSWORD")
					print("[1] Yes\n[2] No")
					confirm = int(input("Proceed to change your password? "))

					if confirm == 1:
						cur_pass = input("Input current password: ")

						if cur_pass == credentials[1]:
							print("Password verified")
							new_pass = input("Input new password (Max 20 characters): ")
							changePassword(credentials[0], new_pass)
						else:
							print("Wrong password")

					elif confirm == 2:
						pass

					else:
						print("Invalid Input")

				elif command == 9:
					# Export database to excel file
					print("Exporting to Excel...")
					exportToExcel()
					print("Process finished")

				elif command == 10:
					# End the session; Back to login page
					print("Logged out")
					session = False	

				else:
					print("Invalid Input")

			elif role == "clerk":
				# Clerk Nav Page
				print("\n[1] Create \n[2] Find\n[3] Update\n[4] Receive\n[5] Change Password\n[6] Export Database to Excel\n[7] Logout")
				command = int(input("Choose Action: "))
				if command == 1:
					# Create Asset Page
					inputAsset()

				elif command == 2:
					# Can only view assets					
					while 1:
						print("\nVIEW ASSETS\n")
						print("[1] View All\n[2] Filter Asset Name\n[3] Filter Location\n[4] Filter Owner\n[5] Filter Status\n[6] Receipt No.\n[0] Back")
						filter_type = int(input("Search by: "))	
						if filter_type >=1 and filter_type <= 6:
							filterAsset(filter_type)
						elif filter_type == 0:
							break
						else:
							print("Invalid input")	

				elif command == 3:
					while 1:
						print("\nUPDATE ASSET\n")
						print("[1] Perform Operation\n[2] Back")
						option = int(input("Option: "))

						# Perform Operation
						if option == 1:
							print("[1] Sold\n[2] Disposed\n[3] Borrowed\n[4] Lent\n[5] Update")
							op_type = int(input("Choose Operation Type: "))

							asset_ID = input("Enter Asset ID: ")

							if getAsset(asset_ID) != None:

								# Get username of user
								username = credentials[0]

								## Get current details of editable fields in asset / set to default
								image = getAssetfield("image", asset_ID)
								name = getAssetfield("name", asset_ID)
								company = getAssetfield("company", asset_ID)
								owner = getAssetfield("owner", asset_ID)
								status = getAssetfield("status", asset_ID)
								unit_loc = getAssetfield("unit_loc", asset_ID)
								price = getAssetfield("price", asset_ID)
								amount = getAssetfield("amount", asset_ID)
								payment_stat = getAssetfield("payment_stat", asset_ID)

								if op_type == 1:
									# since option chosen is sold, set status to sold
									status = "In Transit - Sold"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Sold"
												unit_loc = input("Location: ")
												owner = input("Owner: ")
												recipient = input("Recipient: ") 
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = "Unapproved"

												try:
													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID) #since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 2:
									# since option chosen is disposed, set status to sold
									status = "In Transit - Disposed"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Disposed"
												unit_loc = input("Location: ")
												recipient = input("Recipient: ")
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = "Unapproved"

												try:
													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID) #since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 3:
									# since option chosen is borrowed, set status to sold
									status = "In Transit - Borrowed"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Borrowed"
												unit_loc = input("Location: ")
												recipient = input("Recipient: ")
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = "Unapproved"

												try:
													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID)	#since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 4:
									# since option chosen is lent, set status to sold
									status = "In Transit - Lent"
									try:
										# generate receipt
										print("\nRECEIPT PAGE\n")
										while 1:
											receipt_no = input("Enter receipt number: ")
											if checkReceiptNo(receipt_no) == None:
												op_type = "Lent"
												unit_loc = input("Location: ")
												recipient = input("Recipient: ")
												username = str(credentials[0])
												auth = input("Authorized By: ")
												approval = "Unapproved"

												try:
													createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
													setdefaultImage(receipt_no, asset_ID)	#since no updates to image, copy the stored image
												except Error as error:
													print(error)
												break
											else:
												print("Receipt number already exists.")
										break					
									except Error as error:
										print(error)

								elif op_type == 5:
									check_changes = False 	#initialize changes made to false
									updated_image = False    ##initialize to false
									
									while 1:
										# update other info
										print("\nChoose fields to update")
										print("[1] Asset Name \n[2] Company \n[3] Ownership \n[4] Unit Location\n[5] Amount\n[6] Payment Status\n[7] Image\n[8] Save changes\n[9] Back\nOption (Save changes when done): ")
										update_cmd = int(input())

										# update asset name
										if update_cmd == 1:
											name = input("Edit Asset Name: ")
											check_changes = True
										# update company
										elif update_cmd == 2:
											company = input("Edit Company: ")
											check_changes = True
										# update ownership
										elif update_cmd == 3:
											owner = input("Edit Ownership: ")
											check_changes = True
										# update unit location
										elif update_cmd == 4:
											unit_loc = input("Update Unit Location: ")
											check_changes = True
										# update amount
										elif update_cmd == 5:
											while True:
												try:
													holder = float(input("Update Amount: "))
													if isinstance(holder, float):
														amount = holder
														check_changes = True
														break
												except:
													print("Invalid format for amount")
													pass
										# update payment status
										elif update_cmd == 6:
											while 1:
												print("Payment Status (Choose among the options)")
												print("[1] Paid \n[2] Unpaid \nOption: ")
												pstat_option = int(input())

												if pstat_option == 1:
													payment_stat = "Paid"
													check_changes = True
													break

												elif pstat_option == 2:
													payment_stat = "Unpaid"
													check_changes = True
													break

												else:
													print("Invalid option")
										elif update_cmd == 7:
											print("Upload image of asset")
											holder = input("Enter filepath of image (example: C:\\Users\\Desktop\\image.jpg): ")
											if convertToBinaryData(holder) != False:
												image = convertToBinaryData(holder)
												updated_image = True
												check_changes = True
											else:
												print("Image not found. Please try again")

										elif update_cmd == 8:
											if check_changes == True: 
												try:
													# generate receipt
													print("\nRECEIPT PAGE\n")
													while 1:
														receipt_no = input("Enter receipt number: ")
														if checkReceiptNo(receipt_no) == None:
															op_type = "Update"
															recipient = "None"
															username = str(credentials[0])
															auth = input("Authorized By: ")
															approval = "Unapproved"

															try:
																createReceipt(receipt_no, op_type, username, auth, asset_ID, name, recipient, company, owner, unit_loc, amount, payment_stat, image, approval)
																
																if updated_image == False:
																	setdefaultImage(receipt_no, asset_ID)

																print("Changes successfully sent for approval")
															except Error as error:
																print(error)
															break
														else:
															print("Receipt number already exists.")
													break					
												except Error as error:
													print(error)
											else:
												print("No changes were made.")
											
										elif update_cmd == 9:
											break
										else:
											print("Invalid Input")
								else:
									print("Invalid Input")
							else:
								print("Asset ID not found")
						elif option == 2:
							break
						else:
							print("Invalid Input")

				elif command == 4:
					getInTransit()
					receive = int(input("Enter asset ID to be received: "))
					checkInTransit(receive)

				elif command == 5:
					print("\nCHANGE PASSWORD")
					print("[1] Yes\n[2] No")
					confirm = int(input("Proceed to change your password? "))

					if confirm == 1:
						cur_pass = input("Input current password: ")

						if cur_pass == credentials[1]:
							print("Password verified")
							new_pass = input("Input new password (Max 20 characters): ")
							changePassword(credentials[0], new_pass)
						else:
							print("Wrong password")

				elif command == 6:
					# Export databe to excel file
					print("Exporting to Excel...")
					exportToExcel()
					print("Process finished")


				elif command == 7:
					# End the session; Back to login page
					print("Logged out")
					session = False

				else:
					print("\nInvalid Input\n")

			else:
				print("\nInvalid Input\n")

	# Account does not exist
	else:
		print("Invalid Credentials. Please Try Again")
#'''
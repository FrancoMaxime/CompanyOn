import os
import unicodecsv

class CompagnyOn():
	def __init__(self):
		self.AllUsers = AllUsers(self)
		self.AllCompanies=AllCompanies(self)
		self.AllRoles = AllRoles(self)
		
	def load(self):
		self.AllUsers.load()
		self.AllCompanies.load()
		self.AllRoles.load()

class AllObjects():
	def __init__(self, config):
		self.config = config
		self.elements = {}
	
	def load(self):
		self.check_csv()
		self.load_data()
            
	def check_csv(self):
		if not os.path.exists(self.filename):
			self.create_csv()
			self.load_data()

	def create_csv(self):
		print "flibidi"
		with open(self.filename, 'w') as csvfile:
			csvfile.write(self.fields[0])
			tmp = 1
			while tmp < len(self.fields):
				csvfile.write('\t'+self.fields[tmp])
				tmp = tmp + 1
			csvfile.write('\n')
	
	def load_data(self):
		with open(self.filename) as csvfile:
			reader = unicodecsv.DictReader(csvfile, delimiter="\t")
			for row in reader:
				key = row[self.keyid]
				currObject = self.new_object()
				currObject.data = row
				currObject.id = key
				self.elements[key] = currObject


class Object():
	def __init__(self):
		self.data = {}


class AllUsers(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_user','mail','password','firstname','lastname','id_company', 'remark','phonenumber','id_role','active']
		self.filename = 'csv/users.csv'
		self.keyid = 'id_user'
		
	def new_object(self):
		return User()
				
class User(Object):
	def __init__(self):
		Object.__init__(self)
		
class AllCompanies(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_company','name', 'TVA', 'remark', 'domain','id_coworking']
		self.filename = 'csv/companies.csv'
		self.keyid = 'id_company'
		
	def new_object(self):
		return Company()
				
class Company(Object):
	def __init__(self):
		Object.__init__(self)
		
class AllRoles(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_role','name', 'TVA', 'remark', 'domain']
		self.filename = 'csv/roles.csv'
		self.keyid = 'id_role'
		
	def new_object(self):
		return Role()
				
class Role(Object):
	def __init__(self):
		Object.__init__(self)

import os
import unicodecsv
import useful

class CompagnyOn():
	def __init__(self):
		self.AllUsers = AllUsers(self)
		self.AllCompanies=AllCompanies(self)
		self.AllRoles = AllRoles(self)
		
	def load(self):
		self.AllUsers.load()
		self.AllCompanies.load()
		self.AllRoles.load()
		
	def find_all_from_object(self, object):
		if object.__class__.__name__ == User.__name__:
			return self.AllUsers
		elif object.__class__.__name__ == Compagny.__class__ :
			return self.AllCompanies
		elif object.__class__.__name__ == Role.__class__ :
			return self.AllRoles

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
		
	def save(self, configuration, anUser=None):
		self.data["begin"] = useful.now()
		if anUser != None:
			self.data["user"] = anUser.data['u_id']
		allObjects = configuration.find_all_from_object(self)
		with open(allObjects.filename, "a") as csvfile:
			writer = unicodecsv.DictWriter(csvfile, delimiter='\t', fieldnames=allObjects.fields, encoding="utf-8")
			writer.writerow(self.data)
		return self


class AllUsers(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_user','mail','password','firstname','lastname','id_company', 'remark','phonenumber','id_role','active', 'user', 'rating']
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
		self.fields = ['begin','id_company','name', 'TVA', 'remark', 'domain','id_coworking', 'user']
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
		self.fields = ['begin','id_role','name', 'TVA', 'remark', 'domain', 'user']
		self.filename = 'csv/roles.csv'
		self.keyid = 'id_role'
		
	def new_object(self):
		return Role()
				
class Role(Object):
	def __init__(self):
		Object.__init__(self)
		
class AllConnectedUsers():
    def __init__(self):
        self.users = {}

    def __getitem__(self, key):
        return self.users[key]

    def addUser(self, user):
        self.update()
        mail = user.fields['mail']
        if mail not in self.users:
            self.users[mail] = ConnectedUser(user)
        else:
            self.users[mail].update()

    def update(self):
        updatetime = time.time()
        for mail, connecteduser in self.users.items():
            if (updatetime - connecteduser.datetime) > 900:
                del self.users[mail]

    def isConnected(self, mail, password):
        self.update()
        if mail in self.users:
            user = self.users[mail].cuser
            if user.fields['password'] == password:
                self.users[mail].update()
                return True
        return False

    def getLanguage(self, mail):
        if mail in self.users:
            return self.users[mail].cuser.fields['language']
        return 'english'

    def disconnect(self, mail):
        if mail in self.users:
            del self.users[mail]

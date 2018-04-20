import os

class CompagnyOn():
	def __init__(self):
		self.AllUsers = AllUsers(self)
		#self.AllCompanies=AllCompanies(self)
		#self.AllRoles = AllRoles(self)
		
	def load(self):
		self.AllUsers.load()
		#self.AllCompanies.load()
		#self.AllRoles.load()

class AllObjects():
	def __init__(self, config):
		self.config = config
	
	def load(self):
		self.check_csv()
		#self.loaddata()
            
	def check_csv(self):
		if not os.path.exists(self.filename):
			self.create_csv()

	def create_csv(self):
		print "flibidi"
		with open(self.filename, 'w') as csvfile:
			csvfile.write(self.fields[0])
			tmp = 1
			while tmp < len(self.fields):
				csvfile.write('\t'+self.fields[tmp])
				tmp = tmp + 1
			csvfile.write('\n')
	
	def loaddata():
		print "flip"
		


class AllUsers(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_user','mail','password','firstname','lastname','id_company','id_coworking', 'remark','phonenumber','id_role','active']
		self.filename = 'csv/user.csv'
		
		
		

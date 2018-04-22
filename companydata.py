import os
import unicodecsv
import useful
import alsaaudio, time, audioop
import time
import threading
import requests
import json

class CompagnyOn():
	def __init__(self):
		self.AllUsers = AllUsers(self)
		self.AllCompanies=AllCompanies(self)
		self.AllRoles = AllRoles(self)
		self.AllConnectedUsers = AllConnectedUsers()
		self.AllSpecialities = AllSpecialities(self)
		self.AllRequests = AllRequests(self)
		self.AllMessages = AllMessages(self)
		self.UpdateThread = UpdateThread(self)
		self.TemperatureThread = TemperatureThread(self)
		self.ExtThread = ExtThread(self)
		self.is_threading = True
		
	def load(self):
		self.AllUsers.load()
		self.AllCompanies.load()
		self.AllRoles.load()
		self.AllSpecialities.load()
		self.AllRequests.load()
		self.AllMessages.load()
		self.AllRequests.load_status()
		self.UpdateThread.start()
		self.TemperatureThread.start()
		
	def find_all_from_object(self, object):
		if object.__class__.__name__ == User.__name__:
			return self.AllUsers
		elif object.__class__.__name__ == Company.__name__ :
			return self.AllCompanies
		elif object.__class__.__name__ == Role.__name__ :
			return self.AllRoles
		elif object.__class__.__name__ == Speciality.__name__ :
			return self.AllSpecialities
		elif object.__class__.__name__ == Request.__name__ :
			return self.AllRequests
		elif object.__class__.__name__ == Message.__name__ :
			return self.AllMessages

class AllObjects():
	def __init__(self, config):
		self.config = config
		self.elements = {}
		self.last_id = 0
	
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
		max = 0
		with open(self.filename) as csvfile:
			reader = unicodecsv.DictReader(csvfile, delimiter="\t")
			for row in reader:
				key = int(row[self.keyid])
				if key > max:
					max = key
				currObject = self.new_object()
				currObject.data = row
				currObject.id = key
				self.elements[str(key)] = currObject
		self.last_id = max


class Object():
	def __init__(self):
		self.data = {}
		
	def save(self, configuration, anUser=None):

		if None in self.data:
			del(self.data[None])
		self.data["begin"] = useful.now()
		if anUser != None:
			self.data["user"] = anUser.data['id_user']
		allObjects = configuration.find_all_from_object(self)
		if (not allObjects.keyid in self.data) or (self.data[allObjects.keyid] == ""):
			print "sa bug sa mere la pute"
			self.data[allObjects.keyid] = int(allObjects.last_id) + 1
			allObjects.last_id = int(allObjects.last_id) + 1
		allObjects.elements[str(self.data[allObjects.keyid])] = self
		self.data[allObjects.keyid] = str(self.data[allObjects.keyid])
		with open(allObjects.filename, "a") as csvfile:
			writer = unicodecsv.DictWriter(csvfile, delimiter='\t', fieldnames=allObjects.fields, encoding="utf-8")
			writer.writerow(self.data)
		return self

	def verify(self,data):
		for k,v in data.items():
			if k != 'company' and k != '_name_' and k != '_TVA_' and k != '_domain_' and v == "":
				return False
		return True


class AllUsers(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_user','mail','password','firstname','lastname','id_company', 'remark','phonenumber','id_role','active', 'user', 'rating', 'registration', 'id_speciality', 'nb_rating']
		self.filename = 'csv/users.csv'
		self.keyid = 'id_user'
		
	def new_object(self):
		user = User()
		user.data[self.keyid] = str(self.last_id +1)
		self.last_id += 1
		return user
	
	def get_user(self, mail):
		for myId, user in self.elements.items():
			if user.data['mail'] == mail:
				return user
				
class User(Object):
	def __init__(self):
		Object.__init__(self)
		
	def check_password(self, password):
		return self.data['password'] == password
		
class AllCompanies(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_company','name', 'TVA', 'remark', 'domain','id_coworking', 'user']
		self.filename = 'csv/companies.csv'
		self.keyid = 'id_company'
		
	def new_object(self):
		comp = Company()
		comp.data['id_company'] = str(self.last_id +1)
		self.last_id += 1
		return comp
				
class Company(Object):
	def __init__(self):
		Object.__init__(self)
		
class AllRoles(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_role','name', 'remark', 'domain', 'user']
		self.filename = 'csv/roles.csv'
		self.keyid = 'id_role'
		
	def new_object(self):
		role = Role()
		role.data[self.keyid] = str(self.last_id +1)
		self.last_id += 1
		return role
				
class Speciality(Object):
	def __init__(self):
		Object.__init__(self)
		
class AllSpecialities(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_speciality','name', 'remark', 'user']
		self.filename = 'csv/specialities.csv'
		self.keyid = 'id_speciality'
		
	def new_object(self):
		spec = Speciality()
		spec.data[self.keyid] = str(self.last_id +1)
		self.last_id += 1
		return spec
				
class Role(Object):
	def __init__(self):
		Object.__init__(self)
		
class AllConnectedUsers():
    def __init__(self):
        self.users = {}

    def __getitem__(self, key):
        return self.users[key]

    def add_user(self, user):
        self.update()
        mail = user.data['mail']
        if mail not in self.users:
            self.users[mail] = ConnectedUser(user)
        else:
            self.users[mail].update()

    def update(self):
        updatetime = useful.get_timestamp()
        for mail, connecteduser in self.users.items():
            if (updatetime - connecteduser.datetime) > 900:
                del self.users[mail]

    def is_connected(self, mail, password):
        self.update()
        if mail in self.users:
            user = self.users[mail].cuser
            if user.data['password'] == password:
                self.users[mail].update()
                return True
        return False

    def disconnect(self, mail):
        if mail in self.users:
            del self.users[mail]

class ConnectedUser():
    def __init__(self, user):
        self.cuser = user
        self.datetime = useful.get_timestamp()

    def update(self):
        self.datetime = useful.get_timestamp()


class Request(Object):
	def __init__(self):
		Object.__init__(self)
		
class AllRequests(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_request','subject','id_domain', 'remark', 'status' ,'user', 'helper', 'rated']
		self.filename = 'csv/requests.csv'
		self.keyid = 'id_request'
		self.solved = 0
		self.progress = 0
		self.waiting = 0
		self.total = 0
		
	def new_object(self):
		spec = Request()
		spec.data[self.keyid] = str(self.last_id +1)
		self.last_id += 1
		return spec
	
	def load_status(self):
		for k, v in self.elements.items():
			self.total += 1
			if v.data['status'] == '1' or v.data['status'] == 1:
				self.waiting += 1
			elif v.data['status'] == '2' or v.data['status'] == 2:
				self.progress +=  1
			elif v.data['status'] == '3' or v.data['status'] == 3:
				self.solved += 1
			else :
				print v.data['status']
	
	def get_waiting(self):
		if(self.total > 0):
			return '{0:.2f}'.format((self.waiting / float(self.total))* 100, 2)
		return 0
		
	def get_progress(self):
		if(self.total > 0):
			return '{0:.2f}'.format((self.progress / float(self.total))* 100)
		return 0
		
	def get_solved(self):
		if(self.total > 0) :
			return '{0:.2f}'.format((self.solved / float(self.total))* 100)
		return 0

class Message(Object):
	def __init__(self):
		Object.__init__(self)

class AllMessages(AllObjects):
	def __init__(self, config):
		AllObjects.__init__(self, config)
		self.fields = ['begin','id_message','content','user']
		self.filename = 'csv/messages.csv'
		self.keyid = 'id_message'

	def new_object(self):
		spec = Message()
		spec.data[self.keyid] = str(self.last_id +1)
		self.last_id += 1
		return spec
	def get_message(self, id):
		return self.elements[str(id)]


class Sensor():
	def __init__(self):
		self.value=[]
	
	def add_value(self, value):
		if len(self.value)> 100:
			del self.value[0]
		self.value.append(value)
	
	def last_value(self):
		return self.value[-1]
		
class Sensor2():
	def __init__(self):
		self.temperature=0
		self.humidity=0
		self.lumen= 0
		
class Sensor3():
	def __init__(self):
		self.temperature=0
		self.humidity=0
		self.wind =0
	
		
class UpdateThread(threading.Thread):
    def __init__(self, company):
		threading.Thread.__init__(self)
		self.company = company
		self.sensor = Sensor()
    
    def run(self):
		inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
		inp.setchannels(1)
		inp.setrate(8000)
		inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
		inp.setperiodsize(160)

		while self.company.is_threading:
			moy =0
			for i in range(100):
				l,data = inp.read()
				if l:
					moy += audioop.max(data, 2)
				time.sleep(.01)
			moy /= 100
			self.sensor.add_value(moy)
			moy = 0
			
class TemperatureThread(threading.Thread):
    def __init__(self, company):
		threading.Thread.__init__(self)
		self.company = company
		self.sensor = Sensor2()
    def run(self):
		url = 'https://techofficeopendata.azurewebsites.net/api/Data?DeviceId=12&MaxRow=4'
		headers = {}
		headers['accept'] = 'application/json'
		headers['Authorization'] = '093fb7e2-9387-41ee-babe-08d59f923971'
		while self.company.is_threading:
			r = requests.get(url, headers=headers)
			test = json.loads(r.text)
			for i in range(len(test)):
				if test[i]['sensor']['sensorId'] == 49:
					self.sensor.lumen = test[i]['value']
				if test[i]['sensor']['sensorId'] == 50:
					self.sensor.humidity = test[i]['value']
				if test[i]['sensor']['sensorId'] == 51:
					self.sensor.temperature = test[i]['value']
			time.sleep(1200)
			
class ExtThread():
    def __init__(self, company):
		self.company = company
		self.sensor = Sensor3()

    def loadData(self,pays,ville):
		url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22'+str(ville)+'%2C%20'+str(pays)+'%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
		headers = {}
		r = requests.get(url, headers=headers)
		test = json.loads(r.text)
		self.sensor.humidity = '{0:.2f}'.format(float(test['query']['results']['channel']['atmosphere']['humidity']))
		self.sensor.temperature = '{0:.2f}'.format((float(test['query']['results']['channel']['item']['condition']['temp']) -32 )/1.8)
		self.sensor.wind = '{0:.2f}'.format(float(test['query']['results']['channel']['wind']['speed']))


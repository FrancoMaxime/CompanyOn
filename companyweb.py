import web
import useful
import companydata

class Api:
	def GET(self):
		data = web.input()
		print data
		if 'ville' in data and 'pays' in data:
			company.ExtThread.loadData(data.pays,data.ville)
		else:
			company.ExtThread.loadData("BE","Mons")
		return render.api()


class Refresh:
	def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.refresh(mail)

class Message:
	def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		data = web.input()
		user = company.AllUsers.get_user(mail)
		message = company.AllMessages.new_object()
		message.data['content'] = data.text
		message.data['user'] = data.id
		message.data['begin'] = useful.now()
		message.save(company,user)

		return render.message(mail,message.data['id_message'])


class User:
	def GET(self, id):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		user = company.AllUsers.get_user(mail)
		confirm = company.AllUsers.elements[id]
		if user.data['id_company'] == confirm.data['id_company'] and user.data['id_role'] == '1':
			if confirm.data['active'] == '1':
				confirm.data['active'] = '0'
			else:
				confirm.data['active'] = '1'

			confirm.save(company, user)
		raise web.seeother('/company')

class Profile:
	def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.profile(mail)
	def POST(self):
		data = web.input()
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		elif'_validate_' in data and data['_validate_'] == 'validate':
			user = company.AllUsers.get_user(mail)
			request = company.AllRequests.elements[data['_idrequest_']]
			request.data['status'] = 3
			request.save(company,user)
			if request.data['helper'] != -1:
				company.AllRequests.progress -= 1
			else:
				company.AllRequests.waiting -= 1
			company.AllRequests.solved += 1
		return render.profile(mail)


class Request:
	def GET(self):
		mail = is_connected()

		if mail is None:
			raise web.seeother('/connection')
		return render.request(mail)
	
	def POST(self):
		data = web.input()
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		elif'_request_' in data and data['_request_'] == 'request':
			user = company.AllUsers.get_user(mail)
			request = company.AllRequests.new_object()
			id = -1
			if '_name_' in data and data['_name_'] != "":
				time = useful.now()
				speciality = company.AllSpecialities.new_object()
				speciality.data['begin'] = time
				speciality.data['name'] = data['_name_']
				speciality.save(company,user)
				id = speciality.data['id_speciality']
			if request.verify(data):
				if id == -1:
					id = data['_domain_']
				request.data['subject'] = data['_subject_']
				request.data['id_domain'] = id
				request.data['remark'] = data['_remark_']
				request.data['status'] = 1
				request.data['rated'] = 0
				request.data['helper'] = -1
				request.save(company, user)
				company.AllRequests.total += 1
				company.AllRequests.waiting += 1
			else:
				company.AllRequests.last_id -= 1
			
		return render.index(mail)

class Request_Detail:

	def GET(self,id):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.requestDetail(mail,str(id))
	def POST(self,id):
		mail = is_connected()
		data = web.input()
		if mail is None:
			raise web.seeother('/connection')
		elif '_rated_' in data and data['_rated_'] == 'rated':
			if '_rate_' in data and data['_rate_'] != "":
				user = company.AllUsers.elements[id]
				if user.data['rating'] == 0 or user.data['rating'] == '0':
					user.data['rating'] = data['_rate_']
					user.data['nb_rating'] = 1
				else:
					user.data['rating'] =  int(user.data['rating']) + int(data['_rate_'])
					user.data['nb_rating'] = str(int(user.data['nb_rating']) + 1)
				request = company.AllRequests.elements[data['_requestId_']]
				request.data['rated'] = 1

				user.save(company,user)
				user = company.AllUsers.get_user(data['_mail_'])
				request.save(company,user)
		else:
			user = company.AllUsers.get_user(mail)
			request = company.AllRequests.elements[data['_requestId_']]
			request.data['helper'] = user.data['id_user']
			request.data['status'] = 2
			company.AllRequests.waiting -= 1
			company.AllRequests.progress += 1
			user = company.AllUsers.elements[request.data['user']]
			request.save(company,user)
		raise web.seeother('/index')

class Index:
    def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.index(mail)
        
class Connection:
	def GET(self):
		mail = is_connected()
		if mail is not None:
			raise web.seeother('/index')
		return render.connection('')
	
	def POST(self):
		data = web.input(placeImg={})
		print data.items()
		mail = is_connected()
		if mail is not None:
			raise web.seeother('/')
		elif '_signup_' in data and data['_signup_'] == "signup":
			mail = data['_mail_']
			time = useful.now()
			password = useful.encrypt(data['_password_'],time)
			test = company.AllUsers.get_user(mail)
			user = company.AllUsers.new_object()
			if user.verify(data) and test == None:
				user.data['mail'] = mail
				user.data['password'] = password
				user.data['registration'] = time
				user.data['phonenumber'] = data['_phonenumber_']
				user.data['firstname'] = data['_firstname_']
				user.data['lastname'] = data['_lastname_']
				user.data['active'] = 1
				if data['placeImg'] != {}:
					print "fils de pute de ta race"
					if data.placeImg.filename != '':
						print "mongolooooo"
						filepath = data.placeImg.filename.replace('\\', '/')
						ext = ((filepath.split('/')[-1]).split('.')[-1])
						fout = open('./static/img/users' + str(user.data['id_user']), 'w')
						fout.write(data.placeImg.file.read())
						fout.close()
				if '_name_' in data and data['_name_'] != "":
					comp = company.AllCompanies.new_object()
					comp.data['name'] = data['_name_']
					comp.data['TVA'] = data['_TVA_']
					comp.data['domain'] = data['_domain_']
					comp.data['user'] = user.data['id_user']
					comp.save(company, user)
					user.data['id_company'] = comp.data['id_company']
					user.data['id_role'] = '1'
					user.data['active'] = '1'
				if 'company' in data and data['company'] != "" :
					user.data['id_company'] = data['company']
					user.data['id_role'] = '2'
					user.data['active'] = '0'
				user.data['rating'] = 0
				user.data['nb_rating'] = 0
				user.save(company, user)
			else:
				company.AllUsers.last_id -= 1	
			return render.connection("")
		elif '_login_'in data and data['_login_'] == "login":
			test = connexion(data['_username_'], data['_password_'])
			if test != None and test.data['active'] == '1' :
				infoCookie = data['_username_'] + ',' + test.data['password']
				update_cookie(infoCookie)
				company.AllConnectedUsers.add_user(test)
			elif test != None and test.data['active'] == '0':
				print 'teetetete'
				return render.connection('Compte en attente d activation')
			raise web.seeother('/')
			
class Company:
	def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.company(mail)
		
	def POST(self):
		data = web.input()
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		elif '_select_'in data and data['_select_'] == "select":
			pass	
		
class Sensor:
	def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.sensor()
		
class Disconnect():
    def GET(self):
        mail = is_connected()
        if mail is not None:
            company.AllConnectedUsers.disconnect(mail)
        raise web.seeother('/connection')		
        
def notfound():
    return web.notfound(render.notfound())

def is_connected():
    infoCookie = web.cookies().get('companyon')
    if infoCookie is not None:
        infoCookie = infoCookie.split(',')
        if company.AllConnectedUsers .is_connected(infoCookie[0], infoCookie[1]) is True:
            return infoCookie[0]
    return None

def connexion(username, password):
    user = company.AllUsers.get_user(username)
    if user is not None:
        cryptedPassword = useful.encrypt(password, user.data['registration'])
        if user.check_password(cryptedPassword) is True:
            return user
    return None
    
def update_cookie(infoCookie):
    web.setcookie('companyon', infoCookie, expires=9000)
    
if __name__ == "__main__":
	try:
		web.config.debug = True
		company = companydata.CompagnyOn()
		company.load()
		web.template.Template.globals['data'] = company
		web.template.Template.globals['useful'] = useful
		render = web.template.render('templates/', base='layout')
		urls = (
			'/', 'Index',
			'/index','Index',
			'/home','Index',
			'/connection','Connection',
			'/disconnect', 'Disconnect',
			'/compagny', 'Compagny',
			'/request', 'Request',
			'/request/(.+)','Request_Detail',
			'/profile', 'Profile',
			'/company', 'Company',
			'/user/(.+)', 'User',
			'/rate/(.+)', 'Request_Detail',
			'/message', 'Message',
			'/refresh', 'Refresh',
			'/sensor' , 'Sensor',
			'/api', 'Api'
		)
		app = web.application(urls, globals())
		app.notfound = notfound
		app.run()
	except:
		traceback.print_exc(file=sys.stdout)
	finally:
		print 'fin des threads'
		company.is_threading = False
		company.UpdateThread.join()

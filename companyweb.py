import web
import useful
import companydata



class Index:
    def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.index()
        
class Connection:
	def GET(self):
		mail = is_connected()
		if mail is not None:
			raise web.seeother('/index')
		return render.connection()
	
	def POST(self):
		data = web.input()
		print data.items()
		mail = is_connected()
		if mail is not None:
			raise web.seeother('/')
		elif '_signup_' in data and data['_signup_'] == "signup":
			mail = data['_mail_']
			time = useful.now()
			password = useful.encrypt(data['_password_'],time)
			user = company.AllUsers.new_object()
			test = company.AllUsers.get_user(mail)
			if user.verify(data) and test == None:
				print "je passe ici"
				user.data['mail'] = mail
				user.data['password'] = password
				user.data['registration'] = time
				user.data['phonenumber'] = data['_phonenumber_']
				user.data['firstname'] = data['_firstname_']
				user.data['lastname'] = data['_lastname_']
				user.data['active'] = 1
				if '_name_' in data:
					comp = company.AllCompanies.new_object()
					comp.data['name'] = data['_name_']
					comp.data['TVA'] = data['_TVA_']
					comp.data['domain'] = data['_domain_']
					comp.data['user'] = user.data['id_user']
					comp.save(company, user)
					user.data['id_company'] = comp.data['id_company']
				if 'company' in data:
					user.data['id_company'] = data['company']
				user.save(company, user)	
			return render.connection()
		elif '_login_'in data and data['_login_'] == "login":
			test = connexion(data['_username_'], data['_password_'])
			if test != None :
				infoCookie = data['_username_'] + ',' + test.data['password']
				update_cookie(infoCookie)
				company.AllConnectedUsers.add_user(test)
			raise web.seeother('/')
			
class Company:
	def GET(self):
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		return render.enterprise()
		
	def POST(self):
		data = web.input()
		mail = is_connected()
		if mail is None:
			raise web.seeother('/connection')
		elif '_select_'in data and data['_select_'] == "select":
			pass	
		
class Disconnect():
    def GET(self):
        mail = is_connected()
        if mail is not None:
            companydata.connectedUsers.disconnect(mail)
        raise web.seeother('/')		
        
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
        '/compagny', 'Compagny'
    )
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()

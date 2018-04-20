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
		mail = is_connected()
		if mail is not None:
			raise web.seeother('/')
		elif '_signup_' in data and data['_signup_'] == "signup":

			mail = data['_mail_']
			time = useful.now()
			password = useful.encrypt(data['_password_'],time)
			user = companydata.User()
			if user.verify(data):
				user.data['mail'] = mail
				user.data['password'] = password
				user.data['registration'] = time
				user.data['phonenumber'] = data['_phonenumber_']
				user.data['firstname'] = data['_firstname_']
				user.data['lastname'] = data['_lastname_']
				user.data['active'] = 1
				user.save(company)
			return render.connection()
		
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
        cryptedPassword = useful.encrypt(password, user.fields['registration'])
        if user.checkPassword(cryptedPassword) is True:
            return user
    return None

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
        '/disconnect', 'Disconnect'
    )
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()

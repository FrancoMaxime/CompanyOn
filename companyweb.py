import web
import useful
import companydata as data

class Index:
    def GET(self):
        return render.index('test ta mere')
        
class Connection:
	def GET(self):
		return render.connection('test ta mere')
	
	def POST(self):
		mail = is_connected()
		if mail is not None:
			raise web.seeother('/')
		else:
			data = web.input()
			print data.items()
			mail = data['_username_']
			password = data['_password_']
			connexion(mail,password)
		return render.connection('test ta mere')
		
class Disconnect():
    def GET(self):
        mail = is_connected()
        if mail is not None:
            c.connectedUsers.disconnect(mail)
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
	company = data.CompagnyOn()
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

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
			mail = data['mail']
			password = data['password']
		return render.connection('test ta mere')
		
        
def notfound():
    return web.notfound(render.notfound())

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
        '/connection','Connection'
    )
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()

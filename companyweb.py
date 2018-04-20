import web
import useful
import companydata as data

class index:
    def GET(self):
        return render.index('test ta mere')
        
def notfound():
    return web.notfound(render.notfound())

if __name__ == "__main__":
	web.config.debug = True
	company = data.CompagnyOn()
	company.load()
	test = data.User()
	test.data['mail'] = "mongolotest"
	test.save(company)
	web.template.Template.globals['data'] = company
	web.template.Template.globals['useful'] = useful
	render = web.template.render('templates/', base='layout')
	urls = (
        '/', 'index',
        '/index','index'
    )
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()

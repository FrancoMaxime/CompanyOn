import web
import useful

class index:
    def GET(self):
        return render.index('test ta mere')
        
def notfound():
    return web.notfound(render.notfound())

if __name__ == "__main__":
	web.config.debug = True
	#c.load()
	#web.template.Template.globals['c'] = c
	web.template.Template.globals['useful'] = useful
	layout = web.template.frender('templates/layout.html')
	render = web.template.render('templates/', base=layout)
	urls = (
        '/', 'index'
    )
	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()

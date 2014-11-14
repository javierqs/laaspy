import cherrypy
from app import *

def setup_routes():
    d = cherrypy.dispatch.RoutesDispatcher()
    d.connect('home', '/', controller= MainController(), action="index")
    d.connect('model', '/models/{name}', controller=ModelsController(), action="show")
    d.connect('process', '/models/{name}/process', controller=ModelsController(), action="process", conditions=dict(method=['POST']))
    dispatcher = d
    return dispatcher

if __name__=='__main__':
    conf = {
        '/': {
            'request.dispatch': setup_routes(),
            'tools.staticdir.root': os.path.abspath(os.getcwd())
         }, 
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
         }
    }

    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.server.socket_host = '127.0.0.1'
    cherrypy.server.socket_port = 8081
    cherrypy.quickstart(app)


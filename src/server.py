from flask import Flask, request
from flask_cors import CORS
from flask import Response

from OAIRS import OAIRS

app = Flask(__name__)

CORS(app)

app.config.from_object('settings.Config')
app.debug = app.config['DEBUG']

"""------------------------------------------------------------------------------
LOADS THE AVAILABLE COLLECTIONS FROM THE CKAN API AND CACHES THEM
------------------------------------------------------------------------------"""
@app.before_first_request
def serverInit():
	pass

"""------------------------------------------------------------------------------
PING / HEARTBEAT ENDPOINT
------------------------------------------------------------------------------"""

@app.route('/ping')
def ping():
	return Response('pong', mimetype='text/plain')

#'%s/static/sitemap.xml' % app.root_path
@app.route('/sourcedescription.xml')
@app.route('/capabilitylist.xml')
@app.route('/resourcelist.xml')
def static_from_root():
	oairs = OAIRS(app.config)
	content = None
	if request.path[1:] == 'sourcedescription.xml':
		content = oairs.generateSourceDescription(
			request.url_root
		)
	elif request.path[1:] == 'capabilitylist.xml':
		content = oairs.generateCapabilityList(
			request.url_root
		)
	elif request.path[1:] == 'resourcelist.xml':
		content = oairs.generateResourceList(
			request.url_root
		)
	return Response(content, mimetype='text/xml')

if __name__ == "__main__":
	app.run(host=app.config['APP_HOST'], port=app.config['APP_PORT'])

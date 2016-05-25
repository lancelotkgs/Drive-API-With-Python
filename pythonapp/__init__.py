import json

import flask

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow


app = flask.Flask(__name__)

@app.route('/')
def index():
  file_type="document"
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  if credentials.access_token_expired:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    http_auth = credentials.authorize(httplib2.Http())
    drive_service = discovery.build('drive', 'v3', http_auth)
    files = drive_service.files().list(q="'root' in parents",fields="nextPageToken, files(id, name, mimeType, trashed, webViewLink, fileExtension)").execute()
    items = files.get('files', [])
    return flask.render_template('index.html', files = items, file_url=flask.request.args.get('file_url'), file_type=file_type)

@app.route('/oauth2callback')
def oauth2callback(): 
  	# flow = OAuth2WebServerFlow(client_id='423613277287-c78e5ua452hk5d02ftfb0f0ebckfaco3.apps.googleusercontent.com', client_secret='50Iv1Nnr_syC4jFBOK4BrBwf', scope='https://www.googleapis.com/auth/drive', redirect_uri=flask.url_for('oauth2callback', _external=True))
	flow = client.flow_from_clientsecrets('/var/www/pydrive/pythonapp/client_secrets.json', scope='https://www.googleapis.com/auth/drive', redirect_uri=flask.url_for('oauth2callback', _external=True))
	if 'code' not in flask.request.args:
		auth_uri = flow.step1_get_authorize_url()
		return flask.redirect(auth_uri)
	elif 'code' in flask.request.args:
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		flask.session['credentials'] = credentials.to_json()
		return flask.redirect(flask.url_for('index'))
	else: 
		auth_code = flask.request.args.get('code')
		credentials = flow.step2_exchange(auth_code)
		flask.session['credentials'] = credentials.to_json()
		return "404"

@app.route('/folder/', methods=['GET', 'POST'])
def folder():
  folder_id = flask.request.args.get('id')
  folder_name = flask.request.args.get('name')
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])  
  http_auth = credentials.authorize(httplib2.Http())
  drive_service = discovery.build('drive', 'v3', http_auth)
  files = drive_service.files().list(q="'{0}' in parents".format(folder_id), fields="nextPageToken, files(id, name, mimeType, trashed, webViewLink, fileExtension)").execute()
  items = files.get('files', [])
  return flask.render_template('folder.html', files=items, folder_name=folder_name, folder_id=folder_id, file_url=flask.request.args.get('file_url'))

@app.route('/new')
def new(): 
  credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
  http_auth = credentials.authorize(httplib2.Http())
  drive_service = discovery.build('drive', 'v3', http_auth)
  if flask.request.args.get('folder_id'):
    folder_id = flask.request.args.get('folder_id')
  else: 
    folder_id = 'root'

  file_metadata = {
    'mimeType' : 'application/vnd.google-apps.'+flask.request.args.get('type'),
    'parents': [ folder_id ]
  }
  file = drive_service.files().create(body=file_metadata, fields='id, webViewLink').execute()
  file_url = file.get("webViewLink")
  if flask.request.args.get('folder_id'):
    return flask.redirect(flask.url_for('folder', file_url=file_url, id=folder_id, name=flask.request.args.get('folder_name')))
  return flask.redirect(flask.url_for('index', file_url=file_url))

if __name__ == '__main__':
  import uuid
  app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"
  app.debug = True
  app.run()

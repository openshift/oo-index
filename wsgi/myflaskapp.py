# -*- coding: utf-8 -*-

import os, sys
import ast
import json
from flask import Flask, g, request, session, url_for, redirect, flash, render_template
from flask.ext.github import GitHub as AuthGitHub
import github as PyGitHub
from collections import OrderedDict
import requests

class OOIndexError(Exception):
	'''OO-Index specific errors
	'''

app = Flask(__name__)
app.debug = True

try:
	app.config['GITHUB_CLIENT_ID'] = os.environ['GITHUB_CLIENT_ID']
	app.config['GITHUB_CLIENT_SECRET'] = os.environ['GITHUB_CLIENT_SECRET']
	app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me')
except KeyError, ex:
	app.config['GITHUB_CLIENT_ID'] = 'FAKE-CLIENT-ID'
	app.config['GITHUB_CLIENT_SECRET'] = 'FAKE-CLIENT-SECRET'
	print >>sys.stderr, "Missing config: %s (Please fix)" % ex

try:
	app.config['GITHUB_CALLBACK_URL'] = 'https://' + os.environ['OPENSHIFT_APP_DNS'] + '/login/callback'
except KeyError:
	app.config['GITHUB_CALLBACK_URL'] = 'http://localhost:5000' + '/login/callback'

# set it to point to your own oo-index public repo
app.config['OO_INDEX_GITHUB_USERNAME'] = os.environ.get('OO_INDEX_GITHUB_USERNAME', 'openshift')
app.config['OO_INDEX_GITHUB_REPONAME'] = os.environ.get('OO_INDEX_GITHUB_REPONAME', 'oo-index')
app.config['OO_INDEX_QUICKSTART_JSON'] = os.environ.get('OO_INDEX_QUICKSTART_JSON', 'wsgi/static/quickstart.json').strip('/')
#XXX: we're using quickstart.jon from git repo itself.
#app.config['OO_INDEX_QUICKSTART_JSON'] = os.environ.get('OO_INDEX_QUICKSTART_JSON', 'wsgi/static/quickstart.json')
#
#if not app.config['OO_INDEX_QUICKSTART_JSON'].startswith('/'):
#	if 'OPENSHIFT_REPO_DIR' in os.environ:
#		app.config['OO_INDEX_QUICKSTART_JSON'] = os.path.join(os.environ['OPENSHIFT_REPO_DIR'], app.config['OO_INDEX_QUICKSTART_JSON'])

## Jinja2 filters ########

@app.template_filter('owner_display')
def owner_display(quickstart):
	'''Given a `quickstart`, generate a link to quickstart owner.
	'''
	if quickstart.get('owner_avatar_url'):
		link = '<img alt="{qs[owner_name]}" src="{qs[owner_avatar_url]}" height="20" width="20">{qs[owner_name]}'.format(qs=quickstart)
	elif quickstart.get('owner_name'):
		link = quickstart['owner_name']
	else:
		link = quickstart['owner'].split('/')[-1]
	return '<a href="{qs[owner]}">{link}</a>'.format(qs=quickstart, link=link)

@app.template_filter('short_name')
def short_name(name):
	if name.lower() == 'quickstart':
		return 'QS'
	elif name.lower() == 'cartridge':
		return 'CART'
	else:
		return name

## Quickstart file ########
class Quickstarts:
	'''Parse and cache content of file `quickstarts`.
	'''
	timestamp = 0
	cached = None

	def __init__(self):
		self.path = app.config['OO_INDEX_QUICKSTART_JSON']
		self.data = Quickstarts.cached

		# Read file only if it has changed
		try:
			with open(app.config['OO_INDEX_QUICKSTART_JSON'], 'r') as f:
				st = os.fstat(f.fileno())
				if Quickstarts.cached is not None and st.st_mtime == Quickstarts.timestamp:
					return

				print >>sys.stderr, 'Refreshing' if Quickstarts.cached else 'Reading', self.path
				content = f.read()
				Quickstarts.timestamp = st.st_mtime
		except Exception, ex:
			print >>sys.stderr, "Error loading file %s: %s" % (self.path, ex)
			raise

		try:
			self.data = Quickstarts.cached = ast.literal_eval(content)
		except Exception, ex:
			print >>sys.stderr, "Error parsing file %s: %s" % (self.path, ex)
			raise

	def most_starred(self, count=10):
		return sorted(self.data, key=lambda x: int(x['stargazers']), reverse=True)[:count]

	def most_popular(self, count=10):
		return sorted(self.data, key=lambda x: int(x['watchers']), reverse=True)[:count]

	def latest(self, count=10):
		#TODO: we need a field here to sort by inclusion timestamp
		return self.data[-count:]

## authentication ##########

auth = AuthGitHub(app)

@app.before_request
def before_request():
	try:
		g.user = session['user']
	except KeyError:
		g.user = None

@app.route('/login')
def login():
	return auth.authorize(scope='public_repo')

@app.route('/login/callback')
@auth.authorized_handler
def authorized(token):
	next_url = request.args.get('next') or url_for('index')
	if token is None:
		return redirect(next_url)

	session['token'] = token
	session['user']  = auth.get('user')['login']
	return redirect(next_url)

@auth.access_token_getter
def token_getter():
	return session.get('token')

@app.route('/logout')
def logout():
	session.pop('user', None)
	session.pop('token', None)
	return redirect(url_for('index'))

## views ############

@app.route('/')
def index():
	qs = Quickstarts()
	return render_template('index.html', most_starred=qs.most_starred(), most_popular=qs.most_popular(), latest=qs.latest())

@app.route('/add', methods=['GET', 'POST'])
def add():
	if not g.user:
		return redirect(url_for('login'))

	pr = None
	form_data = {}
	if request.method == 'POST':
		try:
			form_data['type'] = request.form['type']
			form_data['github-username'] = request.form['github-username']
			form_data['github-repository'] = request.form['github-repository']
		except KeyError, ex:
			flash('Missing field: %s' % ex, 'error')
			return render_template('add.html') #, **form_data)
		form_data['alternate-name'] = request.form.get('alternate-name')
		form_data['cartridges'] = request.form.get('cartridges')

		try:
			pr = send_pull_request(form_data)
			flash('Pull Request created', 'info')
		except OOIndexError, ex:
			flash(str(ex), 'error')
		except PyGitHub.GithubException, ex:
			flash(ex.data.get('message', 'Unknown error.'), 'error')
		except Exception, ex:
			flash('%s: %s' % (ex.__class__, ex), 'error')

	return render_template('add.html', pr=pr) #, **form_data)

def _get_tree_element(repo, tree, path):
	for el in tree.tree:
		if el.path == path:
			return el
	raise OOIndexError('Invalid path "%s". Please contact support' % path)

def _read_github_file(username, reponame, filename):
	'''Fork repo and read content of `filename`.
	'''
	print 'Loading file content from %s/%s/%s' % (g.user, reponame, filename)
	gh = PyGitHub.Github(session['token'])
	user = gh.get_user()

	# Get user's oo-index repo, create if not exists
	try:
		repo = user.get_repo(reponame)
	except PyGitHub.UnknownObjectException:
		upstream = '%s/%s' % (username, reponame)
		print '  Forking project %s' % upstream
		user.create_fork(gh.get_repo(upstream))
		repo = None

		for i in range(10):
			try:
				repo = user.get_repo(reponame)
				break
			except PyGitHub.GithubException:
				print '  retry %i...' % i
				time.sleep(2)

		if not repo:
			msg = 'Timeout creating repository. Please try again later.'
			flash(msg, 'error')
			raise OOIndexError(msg)

	head = repo.get_commit('HEAD')
	tree = repo.get_git_tree(head.sha, recursive=True)
	blob = _get_tree_element(repo, tree, filename)
	content = requests.get(blob.url, headers={'Accept': 'application/vnd.github.v3.raw+json'}).json()

	return repo, head, tree, content

def _filter_repo_fields(repo):
	fields = [
		'description',
		'forks',
		'updated_at',
		'type',
		'owner',
		'id',
		'size',
		'watchers',
		'name',
		'language',
		'git_repo_url',
		'created_at',
		'default_app_name',
		'owner_type',
		'stargazers'
	]

	r = OrderedDict([ (k,v) for k,v in repo.raw_data.items() if k in fields ])
	r['stargazers'] = repo.stargazers_count
	r['owner_type'] = repo.owner.type
	r['owner'] = repo.owner.html_url
	return r

def _get_repo_for(username, reponame, token=None):
	if token:
		gh = PyGitHub.Github(token)
	else:
		gh = PyGitHub.Github()
	return gh.get_repo(username + '/' + reponame)

def _read_quickstart_repo(username, reponame):
	print 'Reading quickstart repo metadata %s/%s' % (username, reponame)
	return _filter_repo_fields(_get_repo_for(username, reponame))

def send_pull_request(form_data):
	# read metadata of new quickstart repo
	qs_u = form_data['github-username']
	qs_r = form_data['github-repository']
	qs_n = form_data['alternate-name'] or qs_r
	qs_c = form_data['cartridges'] or []
	qs_t = form_data['type'] or []
	try:
		qs = _read_quickstart_repo(qs_u, qs_r)
		qs['alternate_name'] = qs_n
		qs['cartridges'] = qs_c
		qs['type'] = qs_t
	except PyGitHub.UnknownObjectException:
		raise OOIndexError("Username or repository not found: %s/%s" % (qs_u, qs_r))

	try:
		owner = PyGitHub.Github().get_user(qs_u)
		qs['owner_name']       = owner.name
		qs['owner_avatar_url'] = owner.avatar_url
	except:
		qs['owner_name']       = qs['owner']
		qs['owner_avatar_url'] = ''

	# read content of original quickstar.json
	# fork repo if needed
	u = app.config['OO_INDEX_GITHUB_USERNAME']
	r = app.config['OO_INDEX_GITHUB_REPONAME']
	q = app.config['OO_INDEX_QUICKSTART_JSON']
	repo, head, tree, quickstart = _read_github_file(u, r, q)

	# add quickstart to quickstart.json
	quickstart.append(qs)

	# create new blob with updated quickstart.json
	print "Creating blob...",; sys.stdout.flush()
	new_blob = repo.create_git_blob(json.dumps(quickstart, indent=3, encoding='utf-8'), 'utf-8')

	# create tree with new blob
	element = _get_tree_element(repo, tree, q)
	element = PyGitHub.InputGitTreeElement(path=element.path, mode=element.mode, type=element.type, sha=new_blob.sha)

	if not element:
		flash("File not found: %s/%s/%s" % (u, r, q), "error")
		return

	print "Updating tree...",; sys.stdout.flush()
	new_tree = repo.create_git_tree([ element ], tree)

	# create commit for new tree
	print "Creating commit...",; sys.stdout.flush()
	message = 'Quickstart add request: %s/%s' % (qs_u, qs_r)
	new_commit = repo.create_git_commit(message, new_tree, [ repo.get_git_commit(head.sha) ])

	# create new branch for new commit
	print "Creating branch...",; sys.stdout.flush()
	try:
		new_branch = repo.create_git_ref('refs/heads/%s-%s' % (qs_u, qs_r), new_commit.sha)
	except PyGitHub.UnknownObjectException:
		raise OOIndexError("Username or repository not found: %s/%s" % (qs_u, qs_r))

	# and finally, we send our pull request
	print "Creating pull request...",; sys.stdout.flush()
	upstream = _get_repo_for(u, r, session['token'])
	pr_params = {
		'title': message,
		'body': 'Automatically generated PR for oo-index',
		'base': 'master',
		'head': '%s:%s-%s' % (g.user, qs_u, qs_r),
	}
	pr = upstream.create_pull(**pr_params)
	return pr

##########################
if __name__ == "__main__":
	app.run(debug=True)




@app.route('/products/')
def products_list():
  return 'Listing of all products we have.'

@app.route('/products/<product_id>/')
def product_detail(product_id):
  return 'Detail of product     #{}.'.format(product_id)

@app.route(
  '/products/<product_id>/edit/',
  methods=['GET', 'POST'])
def product_edit(product_id):
  return 'Form to edit product #.'.format(product_id)

@app.route( '/products/create/', methods=['GET', 'POST'])
def product():
  return 'Form to create a new product.'

@app.route('/products/<product_id>/delete/', methods=['DELETE'])
def product_delete(product_id):
    raise NotImplementedError('DELETE')

from flask import Flask, make_response,request
from flask import abort, jsonify, redirect, render_template
from flask import request, url_for
from forms import ProductForm

import json


@app.route('/string/')
def return_string():
  dump = dump_request_detail(request)
  return 'Hello, world!'

@app.route('/object/')
def return_object():
  dump = dump_request_detail(request)
  headers = {'Content-Type': 'text/plain'}
  return make_response(Response('Hello, world! \n' + dump, status=200,
    headers=headers))

@app.route('/tuple/<path:resource>')
def return_tuple(resource):
  dump = dump_request_detail(request)
  return 'Hello, world! \n' + dump, 200, {'Content-Type':
    'text/plain'}


def dump_request_detail(request):
  request_detail = """
## Request INFO ##
request.endpoint: {request.endpoint}
request.method: {request.method}
request.view_args: {request.view_args}
request.args: {request.args}
request.form: {request.form}
request.user_agent: {request.user_agent}
request.files: {request.files}
request.is_xhr: {request.is_xhr}

## request.headers ##
{request.headers}
  """.format(request=request).strip()
  return request_detail

@app.route('/products/create/', methods=['GET', 'POST'])
def product_create():
  """Provide HTML form to create a new product."""
  form = ProductForm(request.form)
  if request.method == 'POST' and form.validate():
    mongo.db.products.insert_one(form.data)
    # Success. Send user back to full product list.
    return redirect(url_for('products_list'))
  # Either first load or validation error at this point.
  return render_template('product/edit.html', form=form)

from bson.objectid import ObjectId

@app.route('/products/<product_id>/')
def product_detail(product_id):
  """Provide HTML page with a given product."""
  # Query: get Product object by ID.
  product = mongo.db.products.find_one({ "_id": ObjectId(product_id) })
  print product
  if product is None:
    # Abort with Not Found.
    abort(404)
  return render_template('product/detail.html',
    product=product)

@app.route('/products/')
def products_list():
  """Provide HTML listing of all Products."""
  # Query: Get all Products objects, sorted by date.
  products = mongo.db.products.find()[:]
  return render_template('product/index.html',
    products=products)

@app.route('/')
def index():
  return redirect(url_for('products_list'))

from flask_login import LoginManager, current_user
from flask_login import login_user, logout_user

from forms import LoginForm
from models import User

app.config['SECRET_KEY'] = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf' # Create your own.
app.config['SESSION_PROTECTION'] = 'strong'

app.config['MONGO_DBNAME'] = flask_db
app.config['MONGO_URI'] =
            "mongodb+srv://flask_username:flask_password@cluster0-hkk9r.mongodb.net/flask_db?retryWrites=true&w=majority"


# Use Flask-Login to track current user in Flask's session.
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
  """Flask-Login hook to load a User instance from ID."""
  u = mongo.db.users.find_one({"username": user_id})
  if not u:
        return None
    return User(u['username'])

# Now we can add the login view in app.py

@app.route('/login/', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('products_list'))
  form = LoginForm(request.form)
  error = None
  if request.method == 'POST' and form.validate():
    username = form.username.data.lower().strip()
    password = form.password.data.lower().strip()
    user = mongo.db.users.find_one({"username": form.username.data})
    if user and User.validate_login(user['password'], form.password.data):
      user_obj = User(user['username'])
      login_user(user_obj)
      return redirect(url_for('products_list'))
    else:
      error = 'Incorrect username or password.'
  return render_template('user/login.html',
      form=form, error=error)

@app.route('/logout/')
def logout():
  logout_user()
  return redirect(url_for('products_list'))

from flask_login import login_required

@app.route('/products/<product_id>/delete/', methods=['DELETE'])
@login_required
def product_delete(product_id):
  #

@app.route('/products/create/', methods=['GET', 'POST'])
@login_required
def product_create():
  #

@app.route(
  '/products/<product_id>/edit/',
  methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
#
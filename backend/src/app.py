import json
from flask import Flask, g, request
from database.db import DatabaseDriver
from sessions import password_login


app = Flask(__name__)

# Configuration
app.config.from_mapping(
    DATABASE="database/site.sqlite",
    INIT_SQL="database/init.sql"
)

# Initialize database
db = DatabaseDriver(app.config['DATABASE'], app.config['INIT_SQL'])

# Connect to the database
def get_db():
    if 'db' not in g:
        g.db = db.conn
    return g.db

def success_response(body, code=200):
    """
    Success response function
    """
    return json.dumps(body), code

def failure_response(message, code=404):
    """
    Failure response function
    """
    error_message = {'error': message}
    return json.dumps(error_message), code

# Close database connection
@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Routes
@app.route('/login', methods=['POST'])
def login():
    # Receive login data from request
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        return failure_response('Username or password not provided', 400)

    # Call password_login function from sessions.py to verify credentials
    user = password_login(username, password)

    # Check if login was successful
    if user:
        return success_response({'message': 'Login successful', 'user': user}, 200)
    else:
        return failure_response('Invalid username or password', 401)

# Add other routes 
# Routes

@app.route('/create-account', methods=['POST'])
def create_user(): 
    # Receive login data from request
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')

    
    pass 

def delete_user(): 
    pass

def update_user():
    pass

if __name__ == '__main__':
    app.run()

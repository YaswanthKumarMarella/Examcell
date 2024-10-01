from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
# from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb+srv://yaswanthkumarmarella14:Yaswanth14@project1.uhjhq.mongodb.net/?retryWrites=true&w=majority&appName=project1"  # Change URI for MongoDB Atlas
uri = "mongodb+srv://yaswanthkumarmarella14:Yaswanth14@project1.uhjhq.mongodb.net/?retryWrites=true&w=majority&appName=project1"
app.secret_key = 'your_secret_key'  # Secret key for session management

# mongo = PyMo  ngo(app)
# users_collection = mongo.project1.eamcell  # Users collection in MongoDB

client = MongoClient(uri)
db = client['examcell']
# Route for the home page
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

# Route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists
        user = db.faculty.find_one({'username': username})
        
        # Validate password
        if user and check_password_hash(user['password'], password):
            session['username'] = username  # Set session
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    
    return render_template('login.html')

# Route for registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        existing_user = db.faculty.find_one({'username': username})
        if existing_user:
            flash('Username already exists. Please try another one.', 'danger')
            return redirect(url_for('register'))

        # Hash the password and store user data in MongoDB
        hashed_password = generate_password_hash(password)
        db.faculty.insert_one({'username': username, 'password': hashed_password})
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route to handle button click and insert data into MongoDB
@app.route('/add_data', methods=['POST'])
def add_data():
    if 'username' in session:
        # Example data to insert into MongoDB
        new_data = {'user': session['username'], 'item': 'Sample Item'}

        # Insert the data into MongoDB
        db.faculty.insert_one(new_data)

        # Return success response
        return jsonify({'success': True, 'message': 'Data added to MongoDB!'})
    else:
        return jsonify({'success': False, 'message': 'You need to log in to add data.'}), 401

# Route for logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have successfully logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
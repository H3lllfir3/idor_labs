from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

# Routes
@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user'] = user.username
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/api/user/<int:id>', methods=['GET'])
def profile_data(id):
    
    current_user = User.query.get(id)
    
    session_user = User.query.filter_by(username=session['user']).first()

    if current_user:

        user_data = {
            'username': current_user.username,
            'address': current_user.address,
            'phone': current_user.phone
        }
        return jsonify(user_data)

    return jsonify({'error': 'Not authenticated or unauthorized'})


@app.route('/profile', methods=['GET'])
def profile_template():
    print("profile_template")
    if 'user' in session:
        username = User.query.filter_by(username=session['user']).first()
        if username:
            return render_template('profile.html', user=username)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()


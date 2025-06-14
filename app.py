from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String())
    name = db.Column(db.String())
    birthday = db.Column(db.Date)
    address = db.Column(db.String())
    username = db.Column(db.String(), unique=True)
    password = db.Column(db.String())

    def age(self):
        today = datetime.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('Users/login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        session['user_id'] = user.id
        return redirect(url_for('profile'))
    else:
        return "Login failed. Invalid username or password."


if __name__ == '__main__':
    app.run(debug=True)

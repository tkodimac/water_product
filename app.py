from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, WaterProductReview
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    reviews = WaterProductReview.query.all()
    return render_template('index.html', reviews=reviews)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists!', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('add_review'))
        else:
            flash('Login failed. Check your email and password.', 'danger')
    
    return render_template('login.html')

@app.route('/add_review', methods=['GET', 'POST'])
@login_required
def add_review():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        ml = request.form['ml']
        review_text = request.form['review']
        
        new_review = WaterProductReview(
            name=name,
            description=description,
            ml=ml,
            review=review_text,
            user_id=current_user.id
        )
        db.session.add(new_review)
        db.session.commit()
        flash('Review added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_review.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This creates the tables if they do not exist
    app.run(debug=True)

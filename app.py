#app.py
import pandas as pd
import logging
import csv
import pickle
import streamlit as st
from flask import Flask, request, session, redirect, url_for, render_template, flash,get_flashed_messages
import psycopg2 #pip install psycopg2 
import requests
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from flask import flash
from flask import jsonify
 

app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Change this to your SMTP server
app.config['MAIL_PORT'] = 587  # Change this to your SMTP server's port
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'moviesineflix@gmail.com'  # Change this to your email
app.config['MAIL_PASSWORD'] = 'jskd ridg wlor kqpl'  # Change this to your email password

mail = Mail(app)
# Load movie data on application startup (optional):
movies_dict = pickle.load(open('static/MLfiles/movies_dict.pkl','rb'))  # Replace with your loading logic
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('static/MLfiles/similarity.pkl','rb')) 
genre_options = [
    "Action", "Adventure", "Animation", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Family", "Foreign Language",
    "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller",
    "Western"
]


 
DB_HOST = "localhost"
DB_NAME = "sampledb"
DB_USER = "postgres"
DB_PASS = "pass123"
 
# Function to establish database connection
def get_db_connection():
    return psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)




@app.route('/')
def prehome():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return render_template('prehome.html')


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/processsurvey', methods=['GET', 'POST'])
def process_survey():
    if request.method == 'POST':
        # Get user-selected movie from the form
        selected_movie = request.form['favorite_movie']

        # Implement your recommendation logic here (replace with actual recommendation function)
        recommended_movies, recommended_movies_posters = recommend(selected_movie)

        # Return a new template (recommendations.html) to display recommendations
        return redirect(url_for('recommendations', selected_movie=selected_movie, recommended_movies=recommended_movies, recommended_movies_posters=recommended_movies_posters))
    else:
        # Handle GET requests (redirect to survey form)
        return render_template('surveyForm.html')

from requests.exceptions import RequestException


 
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        # Open database connection using a context manager
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                account = cursor.fetchone()
                
                if account:
                    password_rs = account['password']
                    if check_password_hash(password_rs, password):
                        session['loggedin'] = True
                        session['id'] = account['id']
                        session['username'] = account['username']
                        return redirect(url_for('home'))
                    else:
                        flash('Incorrect username/password')
                else:
                    flash('Incorrect username/password')
            except psycopg2.Error as e:
                flash('Error: ' + str(e))
                logging.error('Database error occurred: %s', e)
            finally:
                cursor.close()
    session.clear()
    return render_template('login.html',messages=get_flashed_messages(with_categories=True))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        _hashed_password = generate_password_hash(password)
        
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                account = cursor.fetchone()
                
                if account:
                    flash('Account already exists!')
                elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    flash('Invalid email address!')
                elif not re.match(r'[A-Za-z0-9]+', username):
                    flash('Username must contain only characters and numbers!')
                elif not username or not password or not email:
                    flash('Please fill out the form!')
                else:
                    cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
                    conn.commit()
                    flash('You have successfully registered!')

                    # Sending email confirmation
                    msg = Message(subject="Registration Confirmation", sender='moviesineflix@gmail.com', recipients=[email])
                    msg.body = f"Hello {fullname},\n\nThank you for registering at our website!"
                    mail.send(msg)

            except psycopg2.Error as e:
                flash('Error: ' + str(e))
                logging.error('Database error occurred: %s', e)
            finally:
                cursor.close()
    
    return render_template('register.html')

   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
  
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        # Open database connection using a context manager
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute('SELECT * FROM users WHERE id = %s', [session['id']])
                account = cursor.fetchone()
                # Show the profile page with account info
                return render_template('profile.html', account=account)
            except psycopg2.Error as e:
                flash('Error fetching profile information: ' + str(e))
                logging.error('Database error occurred: %s', e)
            finally:
                cursor.close()
    # User is not logged in, redirect to login page
    return redirect(url_for('login'))


@app.route('/flappy_bird')
def flappy_bird():
    # Redirect to the Flappy Bird game page
    return redirect(url_for('static', filename='game1/index.html'))

@app.route('/wordle')
def wordle():
    # Redirect to the Flappy Bird game page
    return render_template('wordle.html')

@app.route('/survey')
def survey():
    # Extract movie titles for the dropdown selection in the form
    movie_options = movies['title'].tolist()
    return render_template('surveyForm.html', movie_options=movie_options)


@app.route('/gameOption')  # Define a new route for gameOption
def game_option():
    return render_template('gameOption.html')  # Render the gameOption.html template

# Submit feedback route
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if request.method == 'POST':
        data = request.json

        movie_name = data.get('movie')
        rating = int(data.get('rating'))
        review = data.get('review')
        username = session.get('username')

        # Debugging: Print or log values
        print("This is from backend side")
        print("Movie Name:", movie_name)
        print("Rating:", rating)
        print("Review:", review)
        print("Username:", username)

        # Open database connection using a context manager
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                cursor.execute("INSERT INTO feedback (movie_name, rating, review, username) VALUES (%s, %s, %s, %s)",
                               (movie_name, rating, review, username))
                conn.commit()
                response = {'status': 'success', 'message': 'Feedback submitted successfully!'}
            except psycopg2.Error as e:
                conn.rollback()
                response = {'status': 'error', 'message': 'Error submitting feedback: ' + str(e)}
                logging.error('Database error occurred: %s', e)
            finally:
                cursor.close()
        session.clear()
        return jsonify(response)

@app.route('/feedbacks')
def user_feedbacks():
    if 'loggedin' in session:
        # Get the username from the session
        username = session['username']
        # Open database connection using a context manager
        with get_db_connection() as conn:
            cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                # Fetch movie_name, rating, review, and created_at for feedbacks submitted by the logged-in user
                cursor.execute("SELECT movie_name, rating, review, created_at FROM feedback WHERE username = %s", (username,))
                feedbacks = cursor.fetchall()
                return render_template('user_feedbacks.html', feedbacks=feedbacks)
            except psycopg2.Error as e:
                flash('Error fetching feedbacks: ' + str(e))
                logging.error('Database error occurred: %s', e)
            finally:
                cursor.close()
    else:
        flash('Please log in to view your feedbacks.')
        return redirect(url_for('login'))

    
    
@app.route('/view_feedback/<string:movie_name>')
def view_feedback(movie_name):
    # Open database connection using a context manager
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cursor.execute("SELECT * FROM feedback WHERE movie_name = %s", (movie_name,))
            feedbacks = cursor.fetchall()
            return render_template('view_feedback.html', movie=movie_name, feedbacks=feedbacks)
        except psycopg2.Error as e:
            flash('Error fetching feedbacks: ' + str(e))
            logging.error('Database error occurred: %s', e)
        finally:
            cursor.close()



def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=08bc87324c4fa8a51ac34eedd432ca4c')
        response.raise_for_status()  # Raise error for unsuccessful requests
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception as e:
        print(f"Error fetching poster for movie_id {movie_id}: {e}")
        return None

# Function to generate movie recommendations (replace with your recommendation logic)
def recommend(movie):
    # Assuming 'movies' and 'similarity' are defined somewhere
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)
        else:
            # If unable to fetch poster, add a placeholder or handle as required
            recommended_movies_posters.append("placeholder_url")
    return recommended_movies, recommended_movies_posters

@app.route('/recommendations')
def recommendations():
    selected_movie = request.args.get('selected_movie')
    recommended_movies, recommended_movies_posters = recommend(selected_movie)
    recommended_data = zip(recommended_movies, recommended_movies_posters)
    return render_template('recommendations.html', selected_movie=selected_movie, recommended_data=recommended_data)

if __name__ == '__main__':
    app.run(debug=True)

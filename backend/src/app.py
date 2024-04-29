from backend.init import app, db
from backend.database.sessions import *
from flask import Flask, g, request
import json


# Check login/logout params
session_messages = []
process_session_params(db, session_messages)


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

# Routes - Test
@app.route("/", methods = ['POST'])
def hello_world():
    return "Hello world!"


# Routes - User Login/Logout Section -----------------
@app.route('/login', methods=['POST'])
def login():
    # Receive login data from request
    username = request.form.get('username')
    password = request.form.get('password')

    # Check if username and password are provided
    if not username or not password:
        return failure_response('Username or password not provided', 400)

    # Call password_login function from sessions.py to verify credentials
    response = password_login(username, password)

    # Check if login was successful
    if response:
        return success_response({'message': 'Login successful', 'user': response}, 200)
    else:
        return failure_response('Invalid username or password', 401)


@app.route('/logout', methods=['POST'])
def logout():
    response = logout()
    if response:
        return success_response({'message': 'Logout successful', 'user': response}, 200)
    else:
        return failure_response('Logout Error', 401)

@app.route('/create-account', methods=['POST'])
def create_user():
    # Receive login data from request
    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    password_confirmation = request.form.get('password-confirmation')
    user = create_account(name, username, password, password_confirmation)
    # Check if create account was successful
    if user:
        return success_response({'message': 'Login successful', 'user': user}, 200)
    else:
        return failure_response('Invalid username or password', 401)


@app.route('/get-all-books', methods=['POST'])
def get_all_books():
    books = db.get_all_books()
    if books:
        return success_response(books)
    return failure_response("No books found")

@app.route('/get-book-by-id/<int:book_id>', methods=['POST'])
def get_book_by_id(book_id):
    book = db.get_book_by_id(book_id)
    if book:
        return success_response(book)
    return failure_response(f"Book with ID {book_id} not found")

@app.route('/get-all-favorites', methods=['POST'])
def get_all_favorites():
    user_id = request.json.get('user_id')
    if not user_id:
        return failure_response("User ID is required")

    favorites = db.get_all_favorites(user_id)
    if favorites:
        return success_response(favorites)
    return failure_response("No favorites found for this user")

@app.route('/favorite-book', methods=['POST'])
def favorite_book():
    # Assuming user_id and book_id are provided in the request
    user_id = request.json.get('user_id')
    book_id = request.json.get('book_id')
    if not user_id or not book_id:
        return failure_response("Both user ID and book ID are required")

    success = db.favorite_book(user_id, book_id)
    if success:
        return success_response({"message": "Book favorited successfully"})
    return failure_response("Failed to favorite book")

@app.route('/unfavorite-book', methods=['POST'])
def unfavorite_book():
    # Assuming user_id and book_id are provided in the request
    user_id = request.json.get('user_id')
    book_id = request.json.get('book_id')
    if not user_id or not book_id:
        return failure_response("Both user ID and book ID are required")

    success = db.unfavorite_book(user_id, book_id)
    if success:
        return success_response({"message": "Book unfavorited successfully"})
    return failure_response("Failed to unfavorite book")

@app.route('/filter-genre', methods=['POST'])
def filter_by_genre():
    # Assuming genre_name is provided in the request
    genre_name = request.json.get('genre_name')
    if not genre_name:
        return failure_response("Genre name is required")

    books = db.filter_by_genre(genre_name)
    if books:
        return success_response(books)
    return failure_response(f"No books found for genre '{genre_name}'")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

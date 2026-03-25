import bcrypt
from pathlib import Path
from app.data.users import add_user, get_user

USER_DATA_FILE = Path('DATA') / 'users.txt'

def migrate_users_to_db(conn):
    with open(USER_DATA_FILE, 'r') as f:
        users = f.readlines()
        for user in users:
            username, password_hash = user.strip().split(',', 1)
            add_user(conn, username, password_hash)

def register_user(conn, username, password):
    """Registers a new user by hashing their password and storing credentials."""
    if not user_exists(conn, username):
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8') 
        add_user(conn, username, hashed_password)
        return True, f"User '{username}' registered successfully!"
    return False, 'Username already exists.'

def user_exists(conn, username):
    """Checks if a username already exists in the user database."""
    user = get_user(conn, username)
    if user is not None:
        return True
    return False

def login_user(conn, username, password):
    """Authenticates a user by verifying their username and password."""
    if not user_exists(conn, username):
        return False, "Username not found."
    _, _, hashed, _ = get_user(conn, username)
    if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
        return True, f"Welcome, {username}!"
    return False, 'Invalid password.'

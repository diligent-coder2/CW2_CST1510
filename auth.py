import bcrypt
import os

USER_DATA_FILE = "DATA\\users.txt"


def hash_password(plain_text_password):
    """Hashes a plain text password with bcrypt."""
    # Encode the password to bytes, required by bcrypt
    password_bytes = plain_text_password.encode('utf-8')
    # Generate a salt and hash the password 
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """Verifies a plain text password."""
    # Encode the plaintext password and hashed_password to bytes
    password_bytes = plain_text_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
	# bcrypt.checkpw() handles extracting the salt and comparing
    if bcrypt.checkpw(password_bytes, hashed_password_bytes):
        return True
    return False

def register_user(username, password):
    """Registers a new user by hashing their password and storing credentials."""
    if not user_exists(username):
        hashed_password = hash_password(password) 
        with open(USER_DATA_FILE, "a") as f: 
            f.write(f"{username},{hashed_password}\n")
        return True
    return False

def user_exists(username):
    """Checks if a username already exists in the user database."""
    if not os.path.exists(USER_DATA_FILE):
        return False

    with open(USER_DATA_FILE, 'r') as f:
        data = f.readlines()
        for d in data:
            if username == d.split(',', 1)[0]:
                return True
    return False

def login_user(username, password):
    """Authenticates a user by verifying their username and password."""
    with open(USER_DATA_FILE, "r") as f: 
        for line in f.readlines():
            user, hashed = line.strip().split(',', 1) 
            if user == username:
	            return verify_password(password, hashed)
            
def validate_username(username):
    """Validates username format."""
    is_valid, error_meassage = False, ''
    if 3 <= len(username) <= 20:
        is_valid = True
        return is_valid, error_meassage
    error_meassage = 'Username is not valid.'
    return is_valid, error_meassage

def validate_password(password):
    """Validates password strength."""
    is_valid, error_meassage = False, ''
 
    if 6 <= len(password) <= 50:
        is_valid = True
        return is_valid, error_meassage
    error_meassage = 'Password is not strong.'
    return is_valid, error_meassage


def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)

def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        choice = input("\nPlease select an option (1-3): ").strip()

        if choice == '1':
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate unique username
            if user_exists(username):
                print('Warning: username already exists.')
                continue
            is_valid, error_msg = validate_username(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()
            # Validate password
            is_valid, error_msg = validate_password(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue

            # Register the user
            if register_user(username, password):
                print(f"Success: User '{username}' registered successfully!")
            else:
                print(f"Error: Username '{username}' already exists.")

        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Check if user exists
            if not user_exists(username):
                print('Error: Username not found.')
                continue

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print("(In a real application, you would now access the homepage.)")
            else:
                print('Error: Invalid password')

            # Optional: Ask if they want to logout or exit
            input("\nPress Enter to return to main menu... ")

        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()

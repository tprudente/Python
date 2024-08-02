import os
import toga
from toga.style.pack import *
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(password):
    """Hashes a password using argon2."""
    return ph.hash(password)

def check_password(password, hashed):
    """Checks a password against a given hash using argon2."""
    try:
        return ph.verify(hashed, password)
    except VerifyMismatchError:
        return False

def button_handler(widget, **kwargs):
    # Path to the file where usernames and hashed passwords are stored
    file_path = 'users.txt'

    # Ensure the users.txt file exists
    if not os.path.exists(file_path):
        open(file_path, 'a').close()

    if widget.text == "Login":
        username = username_input.value.strip()
        password = password_input.value.strip()

        # Read the file and check if the username exists and password matches
        with open(file_path, 'r') as file:
            users = file.readlines()
            for user in users:
                stored_username, stored_hashed_password = user.strip().split(',', 1)
                if stored_username == username:
                    if check_password(password, stored_hashed_password):
                        error_label.text = "Login successful"
                        error_label.style.update(color='green')
                    else:
                        error_label.text = "Incorrect password"
                        error_label.style.update(color='red')
                    return
            error_label.text = "Username not found"
            error_label.style.update(color='red')

    elif widget.text == "Register":
        username = username_input.value.strip()
        password = password_input.value.strip()

        # Read the file and check if the username already exists
        with open(file_path, 'r') as file:
            users = file.readlines()
            for user in users:
                stored_username, _ = user.strip().split(',', 1)
                if stored_username == username:
                    error_label.text = "Username already exists"
                    error_label.style.update(color='red')
                    return

        # If the username does not exist, hash the password and save the new user
        hashed_password = hash_password(password)
        with open(file_path, 'a') as file:
            file.write(f"{username},{hashed_password}\n")
        error_label.text = "User registered successfully"
        error_label.style.update(color='green')

def build(app):
    box = toga.Box()
    global username_input
    global password_input
    global error_label
    # Create username and password input fields
    username_input = toga.TextInput(placeholder='Username', style=Pack(width=200, direction=ROW, alignment=CENTER))
    password_input = toga.PasswordInput(placeholder='Password', style=Pack(width=200, direction=ROW, alignment=CENTER))
    label_user = toga.Label("Username:", style=Pack(width=200, direction=ROW, alignment=CENTER))
    label_pw = toga.Label("Password:", style=Pack(width=200, direction=ROW, alignment=CENTER))

    # Create login and register buttons
    login_button = toga.Button('Login', style=Pack(width=200), on_press=button_handler)
    register_button = toga.Button('Register', style=Pack(width=200), on_press=button_handler)

    # Create boxes for username and password
    username_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER))
    username_box.add(label_user)
    username_box.add(username_input)

    password_box = toga.Box(style=Pack(direction=ROW, alignment=CENTER))
    password_box.add(label_pw)
    password_box.add(password_input)

    # Create error message label
    error_label = toga.Label("", style=Pack(width=200, direction=ROW, alignment=CENTER, color='red'))

    # Add widgets to the main window
    box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER), children=[
        username_box,
        password_box,
        login_button,
        register_button,
        error_label,
    ])

    return box

def main():
    return toga.App("Login", "org.beeware.toga.tutorial", startup=build)

if __name__ == "__main__":
    main().main_loop()

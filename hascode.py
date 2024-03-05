# Example code for generating and saving hashed passwords
import pickle
from pathlib import Path
from getpass import getpass
from hashlib import pbkdf2_hmac
import os

def hash_password(password):
    # Use a secure method to hash the password
    salt = os.urandom(32)
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key

# Get passwords from user
passwords = {
    "pparker": hash_password(getpass("Enter password for pparker: ")),
    "rmiller": hash_password(getpass("Enter password for rmiller: "))
}

# Save hashed passwords to pickle file
file_path = Path(__file__).parent / "hashed_dw.pkl"
with file_path.open("wb") as file:
    pickle.dump(passwords, file)

print("Hashed passwords saved successfully.")

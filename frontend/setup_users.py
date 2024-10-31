import sqlite3
import hashlib

# Function to hash a password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to the database (or create it)
conn = sqlite3.connect('gec_database.db')
cursor = conn.cursor()

# creating a table for users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')

# Add a user (make sure to hash the password)
# CHANGE THE USERNAME AND PASS HERE TO CREATE A NEW USER.
username = "smehta"
password = "mt_app123"
hashed_password = hash_password(password)

cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))

conn.commit()
conn.close()

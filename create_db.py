import sqlite3
import os

# Get the current directory
currentLocation = os.path.dirname(os.path.abspath(__file__))

# Define the correct database path using os.path.join for platform compatibility
db_path = os.path.join(currentLocation, "expenses.db")

# Remove existing corrupt database file (if any)
if os.path.exists(db_path):
    os.remove(db_path)

# Create a fresh database and USERS table with 'email' column
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()

    # Create USERS table with 'email' column and add constraints
    cursor.execute('''
        CREATE TABLE user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,  -- Ensures unique username
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL  -- Ensures unique email
        );
    ''')

    conn.commit()

print("Database and table created successfully with 'email' column!")

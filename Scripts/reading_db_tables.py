
import sqlite3
from sqlite3 import Error


# Step 1: Connect to the database
conn = sqlite3.connect('gec_database.db')  # Replace with your database file name

# Step 2: Create a cursor object
cursor = conn.cursor()

# Step 3: Execute the SELECT query
cursor.execute("SELECT * FROM gec_datapairs")  # Replace with your table name

# Step 4: Fetch all the rows
rows = cursor.fetchall()  # fetchall() retrieves all the rows in the result set

# Print the results
for row in rows:
    print(row)

# Step 5: Close the connection
conn.close()

from flask import Flask, render_template, request, redirect, url_for, make_response         # All necessary imports for making/receiving HTTP requests to the server
from dotenv import load_dotenv                                                              # Useful to load the environment variables from .env files into the Python environment

import pymongo                                                                              # All imports for database management through the back-end
from bson.objectid import ObjectId                                                          # Useful 'ObjectId' class that is a Python representation of MongoDB’s data type for documenting _id fields

import os
import datetime
import sys

# 1. Instantiate the app: 
# The built-in Python variable __name__ refers to the string "__main__". This is exactly lik calling the main() function in any other language. 
# If the Python file within which the __name__ variable is mentioned has been imported into another Python script, it will refer to a string with the name of the imported script file.
# Thus, __name__ makes it easy to determine whether code is running in the main script file or in an imported script file.
app = Flask(__name__)


# 2. Load credentials and configuration options from .env file
# This file is necessary to run the appliaction. It contains sensitive environment variables holding credentials such as the database connection string, username, password, etc. 
# This file should be excluded from version control in the .gitignore file.
load_dotenv()  # Take environment variables from .env.


# 3. Set up the connection to the mongoDB database through pymongo

# We check if the FLASK_ENV is on development through the .env file, we turn on debugging
if os.getenv('FLASK_ENV', 'development') == 'development':
    app.debug = True 

# Connect to the database: 
# You connect through this function ("your_db_host", 27017, username="your_db_username", password="your_db_password", authSource="your_db_name")
# In our case, we load the URI through the .env file through localHost, 27017, username: admin, password: secret, Test_App and a TimeOut server at port 5000
connection = pymongo.MongoClient(os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)
try:
    # Verify the connection works by pinging the database
    connection.admin.command('ping')                # The ping command is cheap and does not require auth.
    db = connection[os.getenv('MONGO_DBNAME')]      # Store a reference to the database
    print(' *', 'Connected to MongoDB!')            # If we get here, the connection worked!

except Exception as err:
    # The ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', err) 


# 4. Setup routes for different HTTP requests 
# @app.route('/')
# def home():


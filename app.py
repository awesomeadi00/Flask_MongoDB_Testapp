from flask import Flask, render_template, request, redirect, url_for, make_response         # All necessary imports for making/receiving HTTP requests to the server
from dotenv import load_dotenv                                                              # Useful to load the environment variables from .env files into the Python environment

import pymongo                                                                              # All imports for database management functions to execute through python
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

# MONGO_DBNAME = your_db_name
# MONGO_URI = "mongodb://your_db_username:your_db_password@your_db_host_server_name:27017/your_db_name?authSource=admin&retryWrites=true&w=majority"
# FLASK_APP = app.py
# FLASK_ENV = development
# GITHUB_SECRET = your_github_secret
# GITHUB_REPO = https://github.com/your-repository-url
dotenv_path = '../app.venv.env'
load_dotenv(dotenv_path)  


# 3. Set up the connection to the mongoDB database through pymongo

# We check if the FLASK_ENV is on development through the .env file, we turn on debugging
if os.getenv('FLASK_ENV', 'development') == 'development':
    app.debug = True 

# Connect to the database: 
# You connect through this function ("your_db_host", 27017, username="your_db_username", password="your_db_password", authSource="your_db_name")
# In our case, we load the URI through the .env file through localHost, 27017, username: admin, password: secret, Test_App and a TimeOut server at port 5000
connection = pymongo.MongoClient(os.getenv('MONGO_URI'))
print("MONGO_URI:", os.getenv('MONGO_URI'), serverSelectionTimeoutMS=5000)

try:
    # Verify the connection works by pinging the database
    connection.admin.command('ping')                # The ping command is cheap and does not require auth.
    database = connection[os.getenv('MONGO_DBNAME')]      # Store a reference to the database
    print('*', 'Connected to MongoDB!')             # If we get here, the connection worked!

except Exception as err:
    # The ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", os.getenv('MONGO_URI'))
    print('Database connection error:', err) 


# 4. Setup routes for different HTTP requests 
# This is the default index route (the home page)
@app.route('/')
def home():
    # Within the database 'messages', we find all of the messages and sort them in descending order of insertion date
    docs = database.messages.find({}).sort("created_at", -1)
    # Then we return the index.html page with all of this information
    return render_template('index.html', docs=docs) # We pass docs = docs as a parameter so that in index.html, they can utilize all the data here and from the database. 

# We create another route where we specify the method as POST as we're going to supply some information (name, message) to the our request to the server
@app.route('/create', methods=['POST'])
def create_post(): 
    # We request the form information from the html page into these variables using flask 
    name = request.form['fname']
    message = request.form['fmessage']

    # We create a new document with this information
    doc = {
        "name": name,
        "message": message,
        "created_at": datetime.datetime.now()
    }

    # We insert this new document into our 'messages' database
    database.messages.insert_one(doc)
    # Makes a request for the / route, so redirects the user back to the home page
    return redirect(url_for('home'))


# We have a route for the Edit Button on every post where we parameterize the route with a specific post_id. This simply renders the edit.html file based on the post_id of the post. 
@app.route('/edit/<post_id>')
def edit(post_id):
    doc = database.messages.find_one({"_id": ObjectId(post_id)})
    return render_template('edit.html', doc=doc) # Also sends the document (the post) to the edit.html file for specifying the data in there. 


# We have another route for the Edit functionality which is called when the User presses the save button on the edit.hml, this updates the database here on the backend. 
@app.route('/edit/<post_id>', methods=['POST'])
def edit_post(post_id): 
    # When the edit button is pressed, it routes here... But the client can't request to the server because the edit.html file isn't loaded. 
    name = request.form['fname']
    message = request.form['fmessage']

    # We update the document with the new name and message
    doc = {
        "name": name,
        "message": message,
        "created_at": datetime.datetime.now()
    }

    # Here, we update one of the elements in the 'messages' database, only the ones which have the id as assigned from the server, so the exact post with that id.
    # the $set operator is used to indicate which fields in the document should be updated, since we're updating the entire document, we just pass the edited 'doc' to the set
    database.messages.update_one(
        {"_id": ObjectId(post_id)},
        {"$set": doc}
    )

    # Once complete, we then make a request to redirect back to the home page '/'
    return redirect(url_for('home'))


# We create another route where we delete a particular post using parameterizing to specify which post to delete
@app.route('/delete/<post_id>')
def delete_post(post_id):
    #Here we delete one element from the 'messages' database which has the the same id as the one prompted by the server. 
    database.messages.delete_one({"_id": ObjectId(post_id)})
    return redirect(url_for('home')) 

# Here we have a final app route which involves any error_handling
# In case the connection to the database in unsuccessful, it passes the Exception and error into this route where it prompts the error.html page
@app.errorhandler(Exception)
def handle_error(err):
    return render_template('error.html', error=err)


# Runs the app, this is what acts as the main() function from the initialization of the __name__ earlier: 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
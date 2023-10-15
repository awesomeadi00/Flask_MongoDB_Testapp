# Flask-MongoDB Web App Example

## Setup for MongoDB:
### Connecting to the database through the Terminal:
Start up a MongoDB database:
- Run `mongosh` on the terminal and make sure there is a database existing already that is used in this code

- Show the available databases: `show dbs`
- Select the database used by this app: `use "database name"`
- Show the documents stored in the `messages` collection: `db.messages.find()` - this will be empty at first, but will later be populated by the app.
- Exit the database shell whenever you have had your fill: `exit`

### Create a `.env` file

A file named `.env` is necessary to run the application. This file contains sensitive environment variables holding credentials such as the database connection string, username, password, etc. This file should be excluded from version control in the [`.gitignore`](.gitignore) file.

An example file named `env.example` is given. Copy this into a file named `.env` and edit the values to match your database. If following the instructions and using Docker to run the database, the values should be as shown in the app.env file:

```
MONGO_DBNAME = testapp_database
MONGO_URI = "mongodb://localhost:27017/testapp_database"
FLASK_APP = app.py
FLASK_ENV = development
GITHUB_SECRET = your_github_secret
GITHUB_REPO = https://github.com/awesomeadi00/Flask_MongoDB_Testapp
```

### Run the app
- Define two environment variables from the command line:
  - On Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
  - On Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
- Start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
- In some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=5000` (or change to `python -m ...` if the `python3` command is not found on your system).
# Flask-MongoDB Web App Example

## Quick test drive
- Install and run [Docker Desktop](https://www.docker.com/get-started)
- Create a [Dockerhub](https://hub.docker.com/signup) account

Start up a MongoDB database:
- Run command, `docker run --name test_app -p 27017:27017 -d mongo:latest`

Start up the app:
- Run command, `docker run -ti --rm -d -p 5000:5000 -e MONGO_DBNAME=test_app -e MONGO_URI="mongodb://admin:secret@host.docker.internal:27017/example?authSource=admin&retryWrites=true&w=majority" test_app/example_application`
- If you see an error about the port number being already in use, change the first `5000` in the command to a different port number, e.g. `-p 10000:5000` to use your computer's port `10000`.

View the app in your browser:
- Open a web browser and go to `http://localhost:5000` (or change `5000` to whatever port number you used in the command above)

## Setup for Editing:
### Connecting to the database through the Terminal:
- Connect to the database server from the command line: `docker exec -ti mongodb_dockerhub mongosh -u admin -p secret`
- Show the available databases: `show dbs`
- Select the database used by this app: `use example`
- Show the documents stored in the `messages` collection: `db.messages.find()` - this will be empty at first, but will later be populated by the app.
- Exit the database shell whenever you have had your fill: `exit`

### Run the app
- Define two environment variables from the command line:
  - On Mac, use the commands: `export FLASK_APP=app.py` and `export FLASK_ENV=development`.
  - On Windows, use `set FLASK_APP=app.py` and `set FLASK_ENV=development`.
- Start flask with `flask run` - this will output an address at which the app is running locally, e.g. https://127.0.0.1:5000. Visit that address in a web browser.
- In some cases, the command `flask` will not be found when attempting `flask run`... you can alternatively launch it with `python3 -m flask run --host=0.0.0.0 --port=5000` (or change to `python -m ...` if the `python3` command is not found on your system).
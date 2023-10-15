# Flask-MongoDB Web App Example

## Quick test drive
- Install and run [Docker Desktop](https://www.docker.com/get-started)
- Create a [Dockerhub](https://hub.docker.com/signup) account

Start up a MongoDB database:
- Run command, `docker run --name test_app -p 12000:27017 -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=secret -d mongo:latest`

Start up the app:
- Run command, `docker run -ti --rm -d -p 12000:5000 -e MONGO_DBNAME=test_app -e MONGO_URI="mongodb://admin:secret@host.docker.internal:27017/example?authSource=admin&retryWrites=true&w=majority" awesomeadi00/test_app`
- If you see an error about the port number being already in use, change the first `12000` in the command to a different port number, e.g. `-p 10000:5000` to use your computer's port `10000`.

View the app in your browser:
- Open a web browser and go to `http://localhost:12000` (or change `12000` to whatever port number you used in the command above)
# Developer Guide

## Setting up a dev environment

### Server Setup

#### Requirements

- Python >= 3.7
- Poetry >= 1.2.2
- Mongodb >= 5.0.0

#### Setup MongoDB

If you do not have mongodb running make sure you have `Docker` installed and run

```bash
# Create a mongodb docker container using mongo image
$ docker container run --name waterdip --publish 27017:27017 -d mongo:5.0.0

# Get access into running mongo container bash
$ docker container exec -it waterdip bash

# Then run mongo by typing following command. it will start the mongo shell
$ mongo

# Create you desired database (ex: wd-dev) with following command
$ use wd-dev

# Then create a user to grant privileges to your database
$ db.createUser({ user: "<USER>", pwd: "<PASSWORD>", roles: [] })

# Exit from the mongo shell by typing exit command. now you are on the bash.
$ exit

# Now enable authentication to created database by typing following command on the bash
$ mongo --port 27017 -u <USER> -p <PASSWORD> --authenticationDatabase wd-dev
```

#### Setup environment variables

Create a `.env` file in the root directory add required configuration

```dotenv
WD_MONGODB_URL=mongodb://<USER>:<PASSWORD>@127.0.0.1/wd-dev
MONGODB_DATABASE=wd-dev
```

#### Run the server

```bash
 # Install python dependencies
 $ poetry install

 # Install dev dependencies
 $ poetry install --with test

 # Start the server
 $ python -m waterdip
```

Afterward, you should be able to access the backend app at **http://localhost:4422/** and swagger docs will be available at **http://localhost:4422/api/docs**

### Frontend Setup

Frontend code is placed under ./frontend package. First we need to go inside frontend directory

```bash
$ cd ./frontend
```

#### Requirements

- node >= v16+

#### Setup environment variables

Create a `.env` file in the root directory and add required configuration

```dotenv
REACT_APP_API_URL=http://127.0.0.1:4422
```

#### Run the node server

```bash
 # Install dependencies
 $ npm install --force

 # Start node server
 $ npm start
```

Afterward, you should be able to access the frontend app at **http://localhost:4433/**

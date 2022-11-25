# Contributing to Waterdip

Thank you for considering contributing to Waterdip!

## How can you contribute?
We welcome both code and non-code contributions. You can:
* Report a bug
* Improve documentation
* Submit a bug fix
* Propose a new feature or improvement
* Contribute a new feature or improvement
* Test Waterdip

## Code contributions
Here is the general workflow:
* Fork the Waterdip repository
* Clone the repository
* Make the changes and commit them
* Push the branch to your local fork
* Make sure that all the tests are passing successfully
* Submit a Pull Request with described changes
* We follow exactly one commit in the pull request. This will help us to have a clean git history

### Useful git commands for fork based development

#### Creating a Fork
```bash
git clone git@github.com:USERNAME/waterdip.git
```

#### Keeping Your Fork Up to Date
```bash
# Add 'upstream' repo to list of remotes
git remote add upstream https://github.com/waterdipAI/waterdip.git

# Verify the new remote named 'upstream'
git remote -v

# Fetch from upstream remote
git fetch upstream

# View all branches, including those from upstream
git branch -va
```

#### Create a Branch
```bash
# Checkout the main branch - you want your new branch to come from master
git checkout main

# Create a new branch named newfeature (give your branch its own simple informative name)
git branch newfeature

# Switch to your new branch
git checkout newfeature
```

#### Cleaning Up Your Work
Prior to submitting your pull request, you might want to do a few things to clean up your branch and make it as simple as possible for the original repo's maintainer to test, accept, and merge your work.

If any commits have been made to the upstream master branch, you should rebase your development branch so that merging it will be a simple fast-forward that won't require any conflict resolution work.
```bash
# Fetch upstream master and merge with your repo's master branch
git fetch upstream
git checkout main
git merge upstream/main

# If there were any new commits, rebase your development branch
git checkout newfeature
git rebase main

```
Now, it may be desirable to squash some of your smaller commits down into a small number of larger more cohesive commits. You can do this with an interactive rebase:

```bash
# Rebase all commits on your development branch
git checkout
git rebase -i main
```


### Additional information
- Waterdip is under active development.
- We are happy to receive a Pull Request for bug fixes or new functions for any section of the platform. If you need help or guidance, you can open an Issue first.
- Because it is in the process of significant refactoring! If you want to contribute, please first come to our [Discord channel](https://discord.gg/dV3DZPzu) for a quick chat.
- We highly recommend that you open an issue, describe your contribution, share all needed information there and link it to a Pull Request.
- We evaluate Pull Requests taking into account: code architecture and quality, code style, comments & docstrings and coverage by tests.

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
$ docker container run --name waterdip --publish 27017:27017 -d mongo::5.0.0

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
# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0
https://github.com/jungleBadger/udacity_coffee_shop/blob/master/troubleshooting/generate_token.md

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

login:
navigate to frontend, cmd run ionic serve, then web browser to localhost:8100

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`

barista(@fsnd.com Kamisama) active jwt:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJuWHNsWDlGbnlHUlE2OU5sTnZTNiJ9.eyJpc3MiOiJodHRwczovL2Z1bGxjb3VudC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNjVhM2MyYWQzMmMwMDEzNTAwYTMzIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNTk1MzgzODQ0LCJleHAiOjE1OTU0NzAyNDQsImF6cCI6InJuUGN3N2k3NFA0NVR5eEc2VGlqN0xhaFQzaE5HejJ4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.krHZhxjEpQ9BQ9ObYHTnzCa_wHruH0iNI9qJC8zdK7jKMypcsxQv_758ZHTHqswAI8lFgEvRYDQIa2-aybzvBspU8FKIwXd21Lr2_0baZB_YqWSfuhvYj_B0TYRYby9H1OiS85TzGmVIoto9iccKGlMyhZFiv9ZN7RDPq7ErQlzp4e7mnNzrve0mG3y7LKbleeF1EgzYCUqgtchhrhgEf02Z-9U4Q4U7T8quXFGVtLJOTTrLXjt51CslgHXiSe9BcvmYU5-wPiTMUB6qMAsu4_DEo1de6VdQMklhDKLTnGnr49dKD-ANiKugl10CJS7bRWd2FtXQN4u_8MHxge2FhA

manager(@fsnd.com Kamisama) active jwt:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJuWHNsWDlGbnlHUlE2OU5sTnZTNiJ9.eyJpc3MiOiJodHRwczovL2Z1bGxjb3VudC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYxNjU5ZDVkZTNiNTkwMDE5MjUwYzJjIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNTk1MzgzODk5LCJleHAiOjE1OTU0NzAyOTksImF6cCI6InJuUGN3N2k3NFA0NVR5eEc2VGlqN0xhaFQzaE5HejJ4Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.b9z2hOfEjOCzcjCPX51VCTt5FVSIJtAuiWTTGgLEjXuVG08mYDiVWFcIvCpudiEouC00jG2sr6xknobz8NwyRfc2ERQJg4puEttMWWyIEaoP1SqhTMG-hOnxakRmm9D25BIQ5rNLoceSUk_9Yce1U2M5Zmfxp3nWEJo6vx8NI0bqUg6NAc6cC6Ba_DyGHV9A9yEBEwuLD2Gjk7DaihEACvClUm2sl3G5iaTuQiWRIEysrjCF82Egt4GCmWnk6wFYY7N6zc48rumn0B3lVYkr0Vj4izED_BDCOQqIb3Ydpt4VuQR-8CwMHjriU7XzG_tDcrrgoDq4SFFAIqbkCwKIiQ
Capstone
-----

### Introduction

Capstone is a casting agency site which illustrates a company that is in the business of matching actors to movies in production.
Capstone gives one ease of seeing actors and movies managed by the company at different access levels.


### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **Angular** for our website's frontend

### Main Files: Project Structure


Overall:
* Models are located in `models.py`.
* Controllers are located in `run.py`.
* The web frontend is located in `frontend/`, 


### Development Setup
## Backend


First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ cd backend
  $ export FLASK_APP=run.py
  $ export FLASK_ENV=development # enables debug mode
  $ python3 run.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)

5. Active endpoints

    | Functionality            | Endpoint                             | Casting assistant  |  Casting Director  | Executive Producer |
    | ------------------------ | -----------------------------        | :----------------: | :----------------: | :----------------: |
    | Fetches a list of actors | GET /actors                          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Fetches a list of movies | GET /movies                          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Fetches a specific actor | GET /actors/&lt;int:id&gt;          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Fetches a specific movie | GET /movies/&lt;int:id&gt;          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Creates an actor         | POST /actor/create                   |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Patches an actor         | PATCH /actors/&lt;int:id&gt;/edit;   |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Delete an Actor          | DELETE /actors/&lt;int:id&gt;;       |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Creates a movie          | POST /movies/create                  |        :x:         |        :x:         | :heavy_check_mark: |
    | Deletes a movie          | DELETE /movies/&lt;int:id&gt;      |        :x:         |        :x:         | :heavy_check_mark: |
    | Patches a movie          | PATCH /movies/&lt;int:id&gt;/edit;   |        :x:         |        :x:         | :heavy_check_mark: |

6. Live project

    - The backend has been deployed to heroku platform [https://capstone-fullstack.herokuapp.com/](https://capstone-fullstack.herokuapp.com/)

7. API Documentation
    - [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/a6577e8792999355c651)
    Run the above collection to test out with appropriate response data for each endpoint

8. Testing 
    run command `$ cd backend` 
                `$ pytest` to run existing tests
                

## Frontend 
  ### This is under development and will be modified before staging
  To run the development frontend end follow these steps.
  ```
  $ cd frontend/
  $ npm i
  $ ng serve

  ```
### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    -    "add:actors",
    -    "add:movie",
    -    "delete:actors",
    -    "delete:movies",
    -    "edit:actor",
    -    "edit:movie",
    -    "view:actors",
    -    "view:movies"

6. Create new roles for:
    - Casting Assistant
      - Can view actors and movies

    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies

    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database
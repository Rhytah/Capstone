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
    | Fetches a specific actor | GET /actors/&lt;int:id&lt;;          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Fetches a specific movie | GET /movies/&lt;int:id&lt;;          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
    | Creates an actor         | POST /actor/create                   |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Patches an actor         | PATCH /actors/&lt;int:id&lt;/edit;   |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Delete an Actor          | DELETE /actors/&lt;int:id&lt;;       |        :x:         | :heavy_check_mark: | :heavy_check_mark: |
    | Creates a movie          | POST /movies/create                  |        :x:         |        :x:         | :heavy_check_mark: |
    | Deletes a movie          | DELETE /movies/&lt;int:id&lt;;       |        :x:         |        :x:         | :heavy_check_mark: |
    | Patches a movie          | PATCH /movies/&lt;int:id&lt;/edit;   |        :x:         |        :x:         | :heavy_check_mark: |

6. Live project

    - The backend has been deployed to heroku platform [https://capstone-fullstack.herokuapp.com/](https://capstone-fullstack.herokuapp.com/)


## Frontend 
  # This is under development and will be modified before staging
  To run the development frontend end follow these steps.
  ```
  $ cd frontend/
  $ npm i
  $ ng serve

  ```
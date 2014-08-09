An project template for creating a web project using Flask, React, and SQL Alchemy

Built from the [flask_angular_template](https://github.com/surgeforward/flask_angular_template) but using React and Browserify instead of Angular.

This template requires node for compiling assets. I use [invoker](http://invoker.codemancers.com/) to start all processes at once for development.

The db commands for interacting with alembic are modified commands from [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) updated to work with Click


### Instructions

#### 1. Clone the project:

    $ git clone git@github.com:surgeforward/flask_react_template.git
    $ cd flask_react_template

#### 2. Create and initialize virtualenv for the project:

    $ mkvirtualenv flask_react_template
    $ pip install -r requirements.txt
    
#### 3. Get node_modules for building assets:

    $ npm install
    
#### 4. Upgrade the database:

    $ python manage.py db upgrade
    
#### 5. Seed the database:

    $ python manage.py db seed

#### 6. Compile Assets:

    $ gulp scripts styles
    
#### 7. Run the development server:

    $ python manage.py runserver
    
#### 8. In another console run the Celery app:

    $ celery -A project.tasks worker





#### Management Commands

Management commands can be listed with the following command:

    $ python manage.py

These can sometimes be useful to manipulate data while debugging in the browser.    


#### Database Migrations

To create a database migration, run the following command:

    $ python manage.py db migrate
    
Then run the upgrade command

    $ python manage.py db upgrade


#### Tests

To run the tests use the following command:

    $ nosetests

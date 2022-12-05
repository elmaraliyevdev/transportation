# Getting Started

First clone the repository from GitHub and switch to the new directory:

    $ git clone git@github.com:elmaraliyevdev/transportation.git
    $ cd transportation
    
Create and activate the virtualenv for your project.

    $ python3 venv venv
    $ source venv/bin/activate
    
Install project dependencies:

    $ pip install -r requirements.txt

Inside a project directory, create a .env file and add the following:

    DEBUG=True
    SECRET_KEY=your_secret_key
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host
    DB_PORT=your_db_port

This project uses PostGIS for spatial data. You can install it on your system with the following commands.

    $ brew install postgis
    $ brew install gdal

Run the following commands to create the database and tables:
    
    $ python manage.py makemigrations
    $ python manage.py migrate

You can now run the development server:

    $ python manage.py runserver

---
**NOTE**

Postman collection is available in the root directory of the project.

---
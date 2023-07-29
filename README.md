# T2A2 - API webserver project

# Overview
The Gym Class Manager is an application designed to manage, store, retrieve and delete members, trainers and information about gym classes.

Developed using Python, the Gym Class Manager can be used with API clients such as Postman or Insomnia.

**Note:** The below only includes documentation on how to download and install. Please refer to the README document in the assignment submission.

# Requirements

You will need:
* [Python](https://www.python.org/downloads/) (minimum Python 3.10.x)
* [PostgreSQL](https://www.postgresql.org/)
* a terminal (Examples: [Terminal (Mac)](https://support.apple.com/en-au/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac), [WSL (Windows)](https://support.apple.com/en-au/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac) or [Ubuntu (Linux)](https://ubuntu.com/tutorials/command-line-for-beginners#3-opening-a-terminal))
* an API client (Examples: [Postman](https://www.postman.com/downloads/) or [Insomnia](https://insomnia.rest/download))

# Installation

1. Go to [github.com/hotteok219/T2A2-apiwebserver](https://github.com/hotteok219/T2A2-apiwebserver).
2. Select **<> Code**.
3. Select **Download ZIP**. A zip file called *T2A2-apiwebserver-main.zip* will be downloaded to your local drive.
4. Extract/unzip the zip file.
5. Open a terminal.
6. Within the terminal, navigate to the directory of the extracted zip file.

Alternatively, you can clone the repository by following these instructions from [GitHub](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

## Prepare the database
1. Install PostgreSQL, if it is not already installed.
2. In the terminal, enter `psql`.
3. Create the database: `CREATE DATABASE <database_name>;`
    * where `<database_name>` should be replaced with `gym_db`.
4. Create the user and password: `CREATE USER <username> WITH PASSWORD '<password>';`
    * where `<username>` is the username of your choice.
    * where `<password>` is the password of your choice.
5. Provide privileges to the newly created user: `GRANT ALL PRIVILEGES ON DATABASE <database_name> to <username>;`
    * where `<database_name>` is taken from step 3
    * where `<username>` is taken from step 4.
6. Connect to the database: `\c <database_name>`
    * where `<database_name>` refers to the name provided in step 3.
    * Alternatively, if you are unable to login as your newly created user, you may need to exit psql and enter `psql -U <username> -h 127.0.0.1 <database_name>`, where `<database_name>` and `<username>` are taken from steps 3 and 4. You will need to enter the password from step 4.
7. Grant all on schema public: `GRANT ALL ON SCHEMA PUBLIC TO <username>;`
    * where `<username>` is from step 4.
8. To exit psql, enter `\q`

## Set up the environment file
1. Duplicate the `.env.sample` file and rename it to `.env`
2. In the `.env` file, after `DATABASE_URL=`, enter the following: `"postgresql+psycopg2://<username>:<password>@localhost:5432/<database_name>"`, where:
    * `<username>` and `<password>` are taken from step 4 of **Prepare the database**
    * `<database_name>` is taken from step 3 of **Prepare the database**.
3. In the same `.env` file, after `SECRET_KEY=`, enter a secret keyword.
4. Save the `.env` file.

## Set up the virtual environment
1. Install Python, if it is not already installed.
2. In the terminal, create the virtual environment: `python3 -m venv .venv`.
*This will create a virtual environment called `.venv`.*
**Note:** You may need to enter `python` instead of `python3` depending on your Python version. It is recommended to run this application on Python 3.
3. Activate the virtual environment: `source .venv/bin/activate`.
4. Install the required packages: `pip3 install -r requirements.txt`.

**Note:** In the terminal:
* to deactivate the virtual environment, enter `deactivate`
* to reactivate the virtual environment, enter `source .venv/bin/activate`

## Populate data
1. In the terminal, activate the virtual environment, if it's been deactivated.
2. Create the database tables: `flask db create`
3. Seed data into the database tables: `flask db seed`
4. To drop the database tables: `flask db drop`

## Run the application
1. After completing the steps above, ensure your virtual environment is active and in the terminal, enter `flask run`.
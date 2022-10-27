# Search Archive and Import

Search Archives' primary task is to import the archive details from the National Archive services and display them on results on demand.

This application consists of two modules(or applications) 1. Search Archives CLI and Search Archives web module 

## Quick Start Guide
### Prerequisite
1. git - Install the latest version of git
2. docker - Install the latest version of docker

### Setup the Database(MySQL)
1. Pull the MySQL version 8.0.31 image from the docker hub and run
```
$ docker run --name db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<root_password> -d mysql:8.0.31
```
2. To create the database
```
$ docker exec -i db mysql -u root -p<root_password> < extra/inital_sql.sql
```
### Build the code
1. Clone the code from GitHub
```
$ git clone https://github.com/thisisckm/search-archives
```
2. Switch to the search-archives folder
```
$ cd search-archives
```
3. Build the docker image as search-archives
```
$ docker build . -t search-archives:latest
```
### Setup the search-archives CLI module
To avoid typing bigger commands like this
docker run --rm --link db:db -e SEARCH_ARCHIVES_DB_PASSWORD=<root_password> search-archives python manage.py --help, using of Shell Alias or shell script or bat script better. Shell Alias is best for this quick start guide.
```
$ alias search-archives="docker run --rm --link db:db -e SEARCH_ARCHIVES_DB_PASSWORD=<root_password> search-archives python manage.py"
```
### Create the database tables 
```
$ search-archives migrate
```
### Host the search-archives web module
```
$ docker run -d --link db:db -e SEARCH_ARCHIVES_DB_PASSWORD=<root_password> -p 8000:8000 --name search-archives search-archives
```

## Usage
### Import the Archive details
To import the Archive details from the National Archive services

``` 
$ search-archives import_archive 251cd289-2f0d-48fc-8018-032400b67a56 
```
### Search for the archive's details
1. On a web browser go to http://localhost:8000
2. Type the valid archive id on the search bar and hit the go button
3. If the archive details for the ID are already imported, then the result will be displayed. Else "No record found" will be displayed.
4. By default the home page displays the latest 10 records imported.

## Running tests
Assuming that the testing process is run on Linux based system. 
### Prerequisite
1. git - Install the latest version of git
2. docker - Install the latest version of docker
3. python 3.10+
4. Python virtualenv if it's not installed already
5. MySQL Client package
### Prepare test enviorment
1. Pull the MySQL version 8.0.31 image from the docker hub and run
```
$ docker run --name db -p 3306:3306 -e MYSQL_ROOT_PASSWORD=<root_password> -d mysql:8.0.31
```
2. To create the database
```
$ docker exec -i db mysql -u root -p<root_password> < extra/inital_sql.sql
```
3. Clone the code from GitHub
```
$ git clone https://github.com/thisisckm/search-archives
```
4. Switch to the search-archives folder
```
$ cd search-archives
```
5. Setup the environment variable
```
$ . extra/env.sh
```
6. Create the python virtualenv and activate it
```
$ python3 -m venv .venv
$ . .venv/bin/activate
```
### Steps to run the tests
The test cases are written using Django testing module. The following command will run the test cases.
```
$ python manage.py test
```

## Limitation
1. Support MySQL as backends database.
2. Don't support python version 2.7.x
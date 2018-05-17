# test_flask_app
Test Flask App

Application is running under Python 3.5 or higher.

Application contains from 2 services.

Aim of the first microservice is getting data from local files.
Data is accessible with `GET /get-address-data` endpoint
Minor errors like incorrect data types are ignored.
Major errors like filesystem errors lead to 500 error.

Aim of the second microservice is putting data from request to local file.
Data saving is accessible with `PUT /put-address-data` endpoint
Major errors like filesystem errors lead to 500 error.

By default both apps run at localhost.
Port for get service is 5001. Port for put service is 5002.
Hosts and ports can be configured with env variables
`GET_SERVICE_HOST`, `GET_SERVICE_PORT`, `PUT_SERVICE_HOST`, `PUT_SERVICE_PORT`

All common operations can be performed with `make` command

### Initial setup
```cd /path/to/the/project
make init
```
This command will create virtualenvs and install required packages.

### Running apps
```cd /path/to/the/project
make run
```
This command will run both apps with default params. If you need other hosts/ports then set env variables.

### Running tests
```cd /path/to/the/project
make run_tests
```
This command will run unit tests for both apps.

### Running linter
```cd /path/to/the/project
make run_flake
```
This command will run flake8 for both apps.

### Cleaning environments
```cd /path/to/the/project
make clean
```
This command will remove virtualens for both apps.

### Integration testing
```cd /path/to/the/project
make run_integration
```
This command will run simple end-to-end test for both apps.

### Stopping apps
```cd /path/to/the/project
make kill
```
This command will stop both apps.

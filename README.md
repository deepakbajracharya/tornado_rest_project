### Implementing REST API using Tornado

The implementation supports creating, updating, deleting and retrieving __Widget__. Widget has id, name, number_of_parts, created_date and updated_date. The create_date, updated_date and id are managed by the server.

### Installation of Python environment

In the root directory of the project, use the following command
to create python virtual environment. Run the following command from the terminal.

```
python3 -m vent pyenv
```

The above command creates __pyenv__ directory for Python 3.

### Activate the python environment
From the root directory which contains __pyenv__, execute the following command.

```
source pyenv/bin/activate
```
The environment has to be activated for the rest of the activities unless explicitly stated.


### Install the required packages.

```
pip install -r requirements.txt
```

### Run flake8 for verifying style

```
flake8 --count --exclude=pyenv,__pycache__ .
```

The above command reports violations if any.

### Run the tests

```
python -m tornado.testing tests2.py
```

### Starting the application

```
python start_app.py
```

The above command runs the application at port 8888.
It can be accessed from the browser at http://localhost:888.
Sample widgets are automatically loaded into the system.

### Testing using __curl__
The application should be already running for the test.

The curl commands can be run from a separate terminal.

1. List widgets
The following curl command lists the widgets alredy loaded
```
curl curl http://localhost:8888/widgets
```

2. Adding a new widget.
curl  http://localhost:8888/widgets -H "Content-Type: application/json" -d '{"name": "shiny widget", "number_of_parts": 3245}'



Note: The system does not enforce __unique__ constraint on __name__ of __Widget__.

3. Retrieve widget by its id.
```
curl  http://localhost:8888/widgets/<id>
```
In the above command, replace __<id>__ with the id of the widget.

4. Delete widget by id.

```
curl -X DELETE http://localhost:8888/widgets/<id>
```
The widget will be deleted if it exists otherwise it errors out (HTTP 500).
```

5. Updating the widget.
```
curl -X PUT http://localhost:8888/widgets/<id> -H "Content-Type: application/json" -d '{"name": "shiny widget", "number_of_parts": 3245}'
```
Specify the __id__ of the widget at the placeholder __<id>__. Similarly name and number_of_parts  can be specified any string and numeric values.

6. Creating the new widget

```
curl -X POST http://localhost:8888/widgets -H "Content-Type: application/json" -d '{"name": "shiny widget", "number_of_parts": 3245}'
```
To create an object, POST is used.

7. Object validation
The __SQLite__ does not enforce max-length validation. The validation is implemented in the service. On validation, there will be HTTP 500 error.

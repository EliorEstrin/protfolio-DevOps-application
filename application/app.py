from flask import Flask, request, render_template, jsonify, make_response
import mongo
import datetime, logging, sys, json_logging


app = Flask(__name__)
json_logging.init_flask(enable_json=True)
json_logging.init_request_instrument(app)

# init the logger as usual
logger = logging.getLogger("application-logger")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

@app.route('/', methods=['GET'])
def index():
    logger.info("Received request for index page")
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def tasks_get():
    """
    Endpoint for retrieving all tasks from the database.

    Returns:
        JSON: The list of all tasks in the database.
    """
    logger.info("Received request for gettint all the tasks")
    tasks = mongo.get_Tasks()
    print(type(tasks))
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def tasks_post():
    """
    Endpoint to add new task.
    
    Method: POST
    URL: /api/tasks
    
    Request Body: JSON object with task details.
    Example:
    {
        "name": "Task 1",
        "description": "Sample task description.",
        "priority": "High",
        "assigned_to": "John Doe"
    }
    
    Success Response:
    Code: 201
    Content: JSON object with success status and id of the added task.
    Example:
    {
        "status": "success",
        "id": "5f4c6569cbc97f0bcb91eabd"
    }
    """
    logger.info("Received request for creating a tasks")
    data = request.get_json()
    print(f"data recived in response is: {data}")
    # saving it to a database
    id = mongo.add_task(data)
    response = jsonify({'status':'success', 'id':f'{id}'})
    response.status_code = 201
    return response

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    """
    Delete a task based on its id.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        HTTP response with either a success status and the id of the deleted task or an error message with appropriate HTTP status code.
    """
    logger.info("Received request for creating a tasks")
    result = mongo.delete_task(task_id)
    if result == "Error: Task not found":
        return result, 404
    elif result == "Error: Invalid task id":
        return result, 400
    else:
        return result, 200

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """
    This endpoint allows to update a specific task.
    ---
    parameters:
        - name: task_id
          type: string
          required: true
          description: id of task that needs to be updated
        - name: request data
          type: json
          required: true
          description: request data should be a json object containing key value pairs
    responses:
        200:
            description: Task updated successfully.
        400:
            description: Invalid task id.
        404:
            description: Task not found.
    """
    data = request.get_json()
    result = mongo.update_task(task_id,data)

    status = ''
    status_code = ''
    print("value of result is")
    print(result)
    if result == "Error: Task not found":
        status_code = 404
        status = 'NotFound'
    elif result == "Error: Invalid task id":
        status_code = 400
        status = 'Invalid'
    else:
        status_code = 200
        status = 'success'

    
    response = jsonify({'status':f"{status}"})
    response.status_code = status_code

    return response


# Get task information with certeain id
@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """
    Endpoint to get the information of a task given its id.
    ---
    parameters:
        - in: path
          name: task_id
          description: the id of the task 
          type: string
          required: true
    responses:
        200:
            description: A JSON object of the task information.
        404:
            description: Task not found.
        400:
            description: Invalid task id.
    """
    task_information = mongo.get_task_with_id(task_id)

    if task_information == "Error: Task not found":
        status_code = 404
    elif task_information == "Error: Invalid task id":
        status_code = 400
    else:
        status_code = 200
    # Make response
    response = jsonify(task_information)
    response.status_code = status_code
    
    return response


# Return all tasks with certein status
@app.route('/api/tasks/status/<status>', methods=['GET'])
def tasks_status(status):
    """
    Retrieve all tasks from the database sorted by priority of the given status
    
    Parameters:
    status (str): Status for sorting tasks. Possible values include 'open', 'in-progress', and 'completed'.

    Returns:
    JSON object: Tasks sorted by priority of the given status.
    """

    tasks = mongo.sort_by_priority(status)
    print(type(tasks))
    return jsonify(tasks)


@app.route('/api/health', methods=['GET'])
def test():
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=true)
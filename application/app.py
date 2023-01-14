from flask import Flask, request, render_template, jsonify, make_response
import mongo


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Return all the tasks from the data base
@app.route('/api/tasks', methods=['GET'])
def tasks_get():
    tasks = mongo.get_Tasks()
    print(type(tasks))
    return jsonify(tasks)

# updates a task based on an id
@app.route('/api/tasks', methods=['POST'])
def tasks_post():
    data = request.get_json()
    print(data)
    task_name = data['task_name']
    description = data['description']
    assigned_to = data['assigned_to']
    priority_level = data['priority_level']
    mongo.add_task(data)
    print(data)
    # Do something with the data, such as saving it to a database
    return 'Task created'


@app.route('/api/health', methods=['GET'])
def test():
    return 'ok'


# Gets id of a task and changes the information in the data base
@app.route('/api/tasks/<int:id>', methods=['PUT'])
def tasks_id(id):
    return 'PUT /api/tasks/<id> not implemented'

# Return all tasks with certein status
@app.route('/api/tasks/{status}', methods=['GET'])
def tasks_status(status):
    return 'GET /api/tasks/{status} not implemented'


if __name__ == '__main__':
    app.run(debug=True)
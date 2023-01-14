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
    #WTF IS IS NOT JSON
    # response = make_response(jsonify(tasks))
    # response.headers['Content-Type'] = 'application/json'
    return jsonify(tasks)
    # return 'GET /api/tasks not implemented'

# updates a task based on an id
@app.route('/api/tasks', methods=['POST'])
def tasks_post():
    return 'POST /api/tasks not implemented'

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
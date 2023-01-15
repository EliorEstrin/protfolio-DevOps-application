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

# create a task 
@app.route('/api/tasks', methods=['POST'])
def tasks_post():
    data = request.get_json()
    print(f"data recived in response is: {data}")
    mongo.add_task(data)
    # Do something with the data, such as saving it to a database
    response = jsonify({'status':'success'})
    response.status_code = 201
    return response

# Deletes task on given ID
@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task_route(task_id):
    result = mongo.delete_task(task_id)
    if result == "Error: Task not found":
        return result, 404
    elif result == "Error: Invalid task id":
        return result, 400
    else:
        return result, 200

# Updates task decription on given ID
@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    description = data['description']

    result = mongo.update_task(task_id,description)

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

    
    response = jsonify({'status':"f{status}"})
    response.status_code = status_code

    return response

   


# Return all tasks with certein status
@app.route('/api/tasks/<status>', methods=['GET'])
def tasks_status(status):
    tasks = mongo.sort_by_priority(status)
    print(type(tasks))
    return jsonify(tasks)







@app.route('/api/health', methods=['GET'])
def test():
    return 'ok'



if __name__ == '__main__':
    app.run(debug=True)
import requests
import json
ENDPOINT = "http://localhost:5000"


def test_can_call_endpoint():
    """
    Test For:  GET /
    Test that the endpoint can be successfully called.

    This function makes a GET request to the endpoint specified in the ENDPOINT variable.
    It then asserts that the response's status code is equal to 200, indicating that the
    request was successful.
    """
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    """
    Test For:  POST /api/tasks
    This function makes a POST request to the endpoint specified in the ENDPOINT variable, passing
    in the single_payload as json data. 

    It asserts that the response's status code is equal to 201 indicating that the task was created successfully. 
    It also asserts that the response contains an 'id' field 
    and a 'success' field in the 'status' field.
    """
    response = requests.post(ENDPOINT + "/api/tasks", json=single_payload)
    data = response.json()
    print(data)
    assert response.status_code == 201
    assert 'id' in data, f"Expected 'id' field in response, but got {data}"
    assert 'success' in data['status'], f"Expected 'id' field in response, but got {data}"

def test_can_get_task():
    """
    Test For:  GET /api/tasks/<task_id>
    Test if the API can get tasks from the database.

    This function first makes a POST request to insert a new task, and then retrieves the task's id from the response.
    It then makes a GET request to the endpoint specified in the ENDPOINT variable, passing in the task's id.
   
    It asserts that the response's status code is equal to 200, indicating that the request was successful.
    It also asserts that the response contains the same values as the payload used to create the task.
    """
    # Insert task
    response = requests.post(ENDPOINT + "/api/tasks", json=single_payload)
    id_data = response.json()['id']
    # Send GET request
    test_get_id_response = requests.get(ENDPOINT + "/api/tasks/" + id_data)
    data = test_get_id_response.json()

    # Check respone containes values of that task
    assert test_get_id_response.status_code == 200
    assert data["_id"] == id_data
    assert data["assignedTo"] == single_payload["assignedTo"]
    assert data["description"] == single_payload["description"]
    assert data["priority"] == single_payload["priority"]
    assert data["taskName"] == single_payload["taskName"]

def test_can_get_tasks():
    """
    Test For: GET /api/tasks

    This function makes a GET request to the endpoint specified in the ENDPOINT variable
    to get all the tasks from the data base.
    It asserts that the response's status code is equal to 200 indicating that the request was successful.

    It also asserts that the task names, descriptions, assignedTo, and priority fields match the payloads inserted 
    in the database.
    """
    # Insert many tasks
    for payload in multiple_payloads:
        insert_payload(payload)
    response = requests.get(ENDPOINT + "/api/tasks")
    respone_data = response.json()
    
    # Iterate over respose
    for payload in multiple_payloads:
        found = False
        for task in respone_data:
            if task["taskName"] == payload["taskName"] and task["description"] == payload["description"] and task["assignedTo"] == payload["assignedTo"] and task["priority"] == payload["priority"]:
                found = True
                break
        assert found, f"Could not find response with correspanding values to payload taskName: {payload['taskName']} in response"
    assert response.status_code == 200


def test_can_delete_task():
    """
    Test For: DELETE /api/tasks/<taskid>

    This function makes a DELETE request to the endpoint specified in the ENDPOINT variable, passing
    in the taskid as a path parameter.
    It asserts that the response's status code is equal to 200 indicating that the task was deleted successfully.
    """
    new_task_id = insert_payload(single_payload)['id']
    response = requests.delete(ENDPOINT + "/api/tasks/" + new_task_id, json=single_payload)
    assert response.status_code == 200


def test_can_update_task():
    """
    Test For: PUT /api/tasks/<task_id>

    This function tests the ability to update a task by making a PUT request to the endpoint specified in the ENDPOINT variable, passing in the taskid as a path parameter and a JSON payload containing the updated task information.
    It asserts that the response contains a 'success' field in the 'status' key and that the status code is 200.
    """
    update_new_task_id = insert_payload(single_payload)['id']


    response = requests.put(ENDPOINT + "/api/tasks/" + update_new_task_id, json=update_payload)
    data = response.json()

    
    assert 'success' in data['status'], f"Expected 'success' field in response, but got {data['status']}"
    assert response.status_code == 200

    # Get the updated task and check if the data matches the expected data
    get_response = requests.get(ENDPOINT + "/api/tasks/" + update_new_task_id)
    get_data = get_response.json()
    assert get_data["_id"] == update_new_task_id, f"Expected an id to be {update_new_task_id}, but got {get_data['_id']}"
    assert get_data['taskName'] == update_payload['taskName'], f"Expected taskName to be {update_payload['taskName']}, but got {get_data['taskName'] }"
    assert get_data['description'] == update_payload['description'], f"Expected description to be {update_payload['description']}, but got {get_data['description'] }"
    assert get_data['assignedTo'] == update_payload['assignedTo'], f"Expected assignedTo to be {update_payload['assignedTo']}, but got {get_data['assignedTo'] }"
    assert get_data['priority'] == update_payload['priority'], f"Expected priority to be {update_payload['priority']}, but got {get_data['priority'] }"


#/api/tasks/<status>'
def test_can_sort_by_status():

    status = "Urgent"

    # Make a GET request to the tasks_status endpoint with a specific status
    response = requests.get(ENDPOINT + '/api/tasks/status/' + status)
    data = response.json()
    
    # Assert that the response is successful (status code 200)
    assert response.status_code == 200
    
    # Assert that the returned data is a list of tasks
    assert type(data) == list

    # Assert that the tasks in the list have the correct status
    for task in data:
        assert task['priority'] == status




def insert_payload(task):
   payload_response = requests.post(ENDPOINT + "/api/tasks", json=task)
   data = payload_response.json()

   return data


# Payloads for functions

single_payload =  {
        "taskName": "Single_Task_Test",
        "description": "This is a Test task",
        "assignedTo": "John Doe",
        "priority": "Urgent"
    }

multiple_payloads = [
    {
        "taskName": "Task_Test1",
        "description": "This is the first test task",
        "assignedTo": "John Doe",
        "priority": "Urgent"
    },
    {
        "taskName": "Task_Test2",
        "description": "This is the second test task",
        "assignedTo": "Jane Doe",
        "priority": "High"
    },
    {
        "taskName": "Task_Test3",
        "description": "This is the third test task",
        "assignedTo": "John Doe",
        "priority": "Medium"
    }
]

update_payload = {
        "taskName": "Single_Task__update_Test",
        "description": "This is a Test to update atask",
        "assignedTo": "John Doe 2",
        "priority": "High"
}



if __name__ == '__main__':
    test_can_update_task()

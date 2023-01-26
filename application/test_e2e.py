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
    test_get_id_response = requests.get(ENDPOINT + "/api/tasks/" + id_data, json=single_payload)
    data = test_get_id_response.json()

    # Check respone containes values of that task
    assert test_get_id_response.status_code == 200
    assert data["_id"] == id_data
    assert data["assignedTo"] == single_payload["assignedTo"]
    assert data["description"] == single_payload["description"]
    assert data["priority"] == single_payload["priority"]
    assert data["taskName"] == single_payload["taskName"]

# Test the the api can return all tasks
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
     #Assert that the task names, descriptions, assignedTo, and priority fields match the payloads inserted
    for task, payload in zip(respone_data, multiple_payloads):
        assert task["taskName"] == payload["taskName"]
        assert task["description"] == payload["description"]
        assert task["assignedTo"] == payload["assignedTo"]
        assert task["priority"] == payload["priority"]

    assert response.status_code == 200



def insert_payload(task):
   requests.post(ENDPOINT + "/api/tasks", json=task)



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




if __name__ == '__main__':
    test_can_get_tasks()

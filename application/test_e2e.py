import requests

ENDPOINT = "http://localhost:5000"

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    data = {
        "taskName": "Task_Test",
        "description": "This is a Test task",
        "assignedTo": "John Doe",
        "priority": "Urgent"
    }
    response = requests.post(ENDPOINT + "/api/tasks", json=data)
    data = response.json
    print(data)

    assert response.status_code == 201

# if __name__ == '__main__':
#     test_index()

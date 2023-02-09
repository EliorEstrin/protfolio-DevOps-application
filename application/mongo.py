from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import os
import sys

def connection():
    """
    Creates a connection to the MongoDB database.
    
    Returns:
        task_collection (pymongo.collection.Collection): A collection for task documents in the database.
    """
    # URL for the data base
    DB_ENDPOINT = os.environ.get('DB_ENDPOINT')
    if DB_ENDPOINT:
        print(f"The value of MY_VAR is: {DB_ENDPOINT}")
    else:
        print("DB_ENDPOINT is not set.")
        # Setting Value for CI
        DB_ENDPOINT = "mongodb://root:example@mongo:27017"
        # sys.exit(1)
        


    # Creating the connection FOR DEV-MODE
    # client = MongoClient("mongodb://root:example@localhost:27017")
    
    # DockerCompose mode
    # client = MongoClient("mongodb://root:example@mongo:27017")
    
    client = MongoClient(DB_ENDPOINT)

    # Creating a data base
    db = client['tasks']
    task_collection = db["task_collection"]
    return task_collection

connection()

def get_Tasks():
    """
    This function retrieves all the tasks stored in the database.
    
    Returns:
    A JSON object that contains all the tasks stored in the database.
    """
    task_collection = connection()
    tasks = task_collection.find()
    tasks = list(tasks)
    for task in tasks:
        task["_id"] = str(task["_id"])
    return json.loads(json.dumps(tasks, indent=4))

def get_task_with_id(task_id):
    """
    get_task_with_id(task_id: str) -> Dict

    This function retrieves a task from the database with a specified ID.

    Parameters:
    task_id (str): the unique identifier of the task.

    Returns:
    Dict: The JSON representation of the task with the specified ID.

    Raises:
    ValueError: If the task ID is invalid.
    KeyError: If the task with the specified ID is not found in the database.

    Example:
        get_task_with_id("5f5e5c7b33b9a913f70be475")
        >>> {
        >>> "_id": "5f5e5c7b33b9a913f70be475",
        >>> "name": "Get groceries",
        >>> "description": "Pick up milk, bread, and eggs",
        >>> "due_date": "2021-05-01",
        >>> "priority": "High"
        >>> }
    """   
    try:
        task_collection = connection()
        task = task_collection.find_one({'_id': ObjectId(task_id)})
        if task is None:
            return "Error: Task not found"
    except:
        return "Error: Invalid task id"

    # Parse it to return a json
    task["_id"] = str(task["_id"])
    return json.loads(json.dumps(task, indent=4))

def add_task(json_data):
    """
    This function adds a task to the database.
    
    Parameters:
        json_data (dict): A dictionary representing the task.
    
    Returns:
        str: The ID of the inserted task.
    """
    task_collection = connection()
    result = task_collection.insert_one(json_data)
    return result.inserted_id

def delete_task(task_id):
    """
    Delete a task with a specific id
    
    Parameters:
        task_id (str): The id of the task to delete.
        
    Returns:
        str: "Item Deleted" if task was deleted successfully.
             "Error: Task not found" if task with the specified id was not found.
             "Error: Invalid task id" if the id provided was invalid.
    """
    task_collection = connection()
    try:
        result = task_collection.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count == 0:
            return "Error: Task not found"
        return "Item Deleted"
    except:
        return "Error: Invalid task id"

def update_task(task_id, new_data):
    """
    This function updates a task with a given task ID in the database with new data.

    Parameters:
        task_id (str): The ID of the task to update.
        new_data (dict): The new data to update the task with.

    Returns:
        str: A string indicating the result of the update operation. 
        Possible values are:
            - "Error: Task not found": If the task with the given ID was not found in the database.
            - "Error: Invalid task id": If the task ID provided is not a valid ObjectId.
            - "Item was updated": If the task was successfully updated.

    """
    task_collection = connection()
    try:
        result = task_collection.update_one({'_id': ObjectId(task_id)}, {'$set': new_data})
        if result.matched_count == 0:
            return "Error: Task not found"
        return "Item was updated"
    except:
        return "Error: Invalid task id"

def sort_by_priority(priority):
    """
    The sort_by_priority function takes in a priority argument, which is a string.
    It creates a connection to the MongoDB database and retrieves the task collection.

    The function then queries the task collection for tasks that have a matching priority field and stores the result in the tasks variable. The tasks result is converted to a list and each task's _id field is converted to a string.

    Finally, the function returns a JSON representation of the list of tasks.
    """
    task_collection = connection()
    tasks = task_collection.find({"priority": priority})
    tasks = list(tasks)
    for task in tasks:
        task["_id"] = str(task["_id"])
    return json.loads(json.dumps(tasks, indent=4))


### For Testing ###
def add_sample_data():
    task_collection = connection()

    sample_data = [{
        "taskName": "Task 1",
        "description": "This is the first task",
        "assignedTo": "John Doe",
        "priority": "Urgent"
    }, {
        "taskName": "Task 2",
        "description": "This is the second task",
        "assignedTo": "Jane Smith",
        "priority": "Optinal"
    }]
    task_collection.insert_many(sample_data)

data = {
        "taskName": "Task_Test99",
        "description": "This is a Test taska",
        "assignedTo": "John Doe",
        "priority": "Urgent"
    }

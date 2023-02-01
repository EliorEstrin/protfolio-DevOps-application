from pymongo import MongoClient
from bson import json_util, ObjectId

import json



# Connect to db and creates a db name tasks
def connection():
    # Creating the connection FOR DEV-MODE
    client = MongoClient("mongodb://root:example@localhost:27017")
    
    # DockerCompose mode
    # client = MongoClient("mongodb://root:example@mongo:27017")

    # Creating a data base
    db = client['tasks']
    task_collection = db["task_collection"]
    return task_collection


def get_Tasks():
    task_collection = connection()
    tasks = task_collection.find()
    tasks = list(tasks)
    for task in tasks:
        task["_id"] = str(task["_id"])
    return json.loads(json.dumps(tasks, indent=4))


# Get task with spesific id
def get_task_with_id(task_id):
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
    task_collection = connection()
    result = task_collection.insert_one(json_data)
    return result.inserted_id

# Delete tasks
def delete_task(task_id):
    task_collection = connection()
    try:
        result = task_collection.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count == 0:
            return "Error: Task not found"
        return "Item Deleted"
    except:
        return "Error: Invalid task id"

# Update tasks from db
# def update_task(task_id,new_description):
#     # Get Data
#     # Print data
#     task_collection = connection()
#     try:
#         result = task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"description": new_description}})
#         if result.matched_count == 0:
#             return "Error: Task not found"
#         return "Item was updated"
#     except:
#         return "Error: Invalid task id"


def update_task(task_id, new_data):
    task_collection = connection()
    try:
        result = task_collection.update_one({'_id': ObjectId(task_id)}, {'$set': new_data})
        if result.matched_count == 0:
            return "Error: Task not found"
        return "Item was updated"
    except:
        return "Error: Invalid task id"




def sort_by_priority(priority):
    task_collection = connection()
    tasks = task_collection.find({"priority": priority})
    tasks = list(tasks)
    for task in tasks:
        task["_id"] = str(task["_id"])
    return json.loads(json.dumps(tasks, indent=4))



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



# add_sample_data()
# print(sort_by_priority("Urgent"))

# Dev ADD task
data = {
        "taskName": "Task_Test99",
        "description": "This is a Test taska",
        "assignedTo": "John Doe",
        "priority": "Urgent"
    }
# print(add_task(data))

# print(get_task_with_id("63d24cbe9ebd14e0487529a2"))

# print(update_by_json("63da4e32450fc118963dd6df",data))
from pymongo import MongoClient
# import bson.json_util as json_util
# from bson import ObjectId
from bson import json_util, ObjectId

import json



# Connect to db and creates a db name tasks
def connection():
    # Creating the connection
    client = MongoClient("mongodb://root:example@localhost:27017")
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


def add_task(json_data):
    task_collection = connection()
    task_collection.insert_one(json_data)

# Delete tasks
def delete_task(task_id):
    task_collection = connection()
    try:
        result = task_collection.delete_one({'_id': ObjectId(task_id)})
        if result.deleted_count == 0:
            return "Error: Task not found"
        return "Item deleted"
    except:
        return "Error: Invalid task id"

# Update tasks from db
def update_task(task_id,new_description):
    task_collection = connection()
    try:
        result = task_collection.update_one({"_id": ObjectId(task_id)}, {"$set": {"description": new_description}})
        if result.matched_count == 0:
            return "Error: Task not found"
        return "Item was updated"
    except:
        return "Error: Invalid task id"


#print(update_task('63c41396c20b76dcc47be361','test22'))



def sort_by_priority(priority):
    pass




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


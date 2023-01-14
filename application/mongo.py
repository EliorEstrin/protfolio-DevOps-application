from pymongo import MongoClient
from bson import json_util

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
    print(json_util.dumps(tasks, default=json_util.default))
    return json_util.dumps(tasks, default=json_util.default)
    # return tasks
    # tasks = task_collection.find()
    # tasks = [task for task in task_collection.find()]
    # return tasks

    # 



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




all_task = get_Tasks()
print(all_task)
# for task in all_task:
#     print(task)






#isting all the databases
# print(client.list_database_names())
# # Accessing the collection
# coll = db.myCollection
# coll.insert_one({'name': 'John', 'age': 29})


# for doc in coll.find():
#     print(doc)


# # Listing all the collections
# print(db.list_collection_names())
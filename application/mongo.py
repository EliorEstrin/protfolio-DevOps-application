from pymongo import MongoClient

# Connect to db and creates a db name tasks
def connection():
    # Creating the connection
    client = MongoClient("mongodb://root:example@localhost:27017")
    # Creating a data base
    db = client['tasks']
    return db


def get_Tasks():
    db = connection()
    task_collection = db["task_collection"]
    tasks = task_collection.find()
    return tasks



def add_sample_data():
    db = connection()
    task_collection = db["task_collection"]
    sample_data = [{
        "taskName": "Task 1",
        "description": "This is the first task",
        "assignedTo": "John Doe",
        "status": "Not Started"
    }, {
        "taskName": "Task 2",
        "description": "This is the second task",
        "assignedTo": "Jane Smith",
        "status": "In Progress"
    }]
    task_collection.insert_many(sample_data)

# add_sample_data()




# all_task = get_Tasks()
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
from pymongo import MongoClient

# Connect to db and creates a db name tasks
def connection():
    # Creating the connection
    client = MongoClient("mongodb://root:example@localhost:27017")
    # Creating a data base
    db = client['tasks']

    return db
# db.create_collection('myCollection')


connection()


#isting all the databases
# print(client.list_database_names())
# # Accessing the collection
# coll = db.myCollection
# coll.insert_one({'name': 'John', 'age': 29})


# for doc in coll.find():
#     print(doc)


# # Listing all the collections
# print(db.list_collection_names())
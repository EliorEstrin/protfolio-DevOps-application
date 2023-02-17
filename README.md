# Welcome

## Prerequisites
- docker

## about the application

this repository is a python based application developed in a REST api fassion.
the purpose of this application to manage tasks.
it has the route belows:

- GET /api/tasks - returns all tasks
- POST /api/tasks - adds a task
- GET /api/tasks/<id> - gets a specific task based on an id
- PUT /api/tasks/<id> - update a specific task based on id

the application is connected to a mongodb database that saves the data in a uniqe collection.


## Installation and Running the Application

1. Clone the repository:
```
git clone https://github.com/elior7557/task-managment-app.git
 ```

2. Change into the project directory:
```
cd task-managment-app/app
```
3. Start the application with docker-compose
```
docker compose up -d
```


Open your web browser and navigate to http://localhost:5000 to access the application.

## another files in this repo:

test_e2e.py - file for testing the application using pytest. it has test for each route 
this repo contains as well a `.github worklows` folder which contains the CI-CD for this applcation

### Steps of CI-CD
1. Clone 
2. build - build the application code using docker-compose
3. test - testing the application using pytest
4. calculate version and publish - calculating the version based on the recent tag and publishing the image to a private dockerhub repository
5. deploy - update to gitops repository which is currently private, and then argocd deploys the application


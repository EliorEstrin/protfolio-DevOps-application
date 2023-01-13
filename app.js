const option_create_btn = document.querySelector("#option_create");
var btn = document.querySelector('#create_task_button');
// const addTaskBtn = document.querySelector("#add-task-btn");
// const taskList = document.querySelector("#task-items");

function hideCreateTask() {
    var createTask = document.querySelector('#create-task-form');
    createTask.style.display = 'none';
  }

function showCreateTask() {
var createTask = document.querySelector('#create-task-form');
createTask.style.display = 'inline-block';
}



function hideAll(){
    hideCreateTask()
}
// hideAll()


option_create_btn.addEventListener('click', showCreateTask)
btn.addEventListener('click', hideCreateTask);

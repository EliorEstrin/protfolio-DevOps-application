// Definitation of btn that acced later in the code
const option_create_btn = document.querySelector("#option_create");
const submit_create_btn = document.querySelector('#create_task_button');

// by deafult:
hideAll()



// Funtion to hide all form elements that created afer a btn is pressed
// Usefull when the page reload after a form get submitted
function hideAll(){
    hideCreateTask()
}

// gets an element and shows him on the page
function showForm(element_id) {
    var element = document.querySelector(element_id);
    element.style.display = 'inline-block';

}



// option_create_btn.addEventListener('click', showCreateTask)
option_create_btn.addEventListener('click', () => showForm('#create-task-form'));


// After submitted form can be removed
submit_create_btn.addEventListener('click', hideCreateTask);



function hideCreateTask() {
    var createTask = document.querySelector('#create-task-form');
    createTask.style.display = 'none';
}

function showCreateTask() {
var createTask = document.querySelector('#create-task-form');
createTask.style.display = 'inline-block';
}
// Definitation of btn that acced later in the code
//Options
const option_create_btn = document.querySelector("#option_create");
const option_delete_btn = document.querySelector("#option_delete");
const option_edit_btn = document.querySelector("#option_edit");
const option_update_btn = document.querySelector("#option_update");

//Sumbit btn
const submit_create_btn = document.querySelector('#create_task_btn');
const submit_delete_btn = document.querySelector('#delete_task_btn');


// by deafult:
hideAll()



// Funtion to hide all form elements that created afer a btn is pressed
// Usefull when the page reload after a form get submitted
function hideAll(){
    hideForm('#create-task-form')
    hideForm('#delete-task-form')
}

// gets an element and shows him on the page
function showForm(element_id) {
    hideAll()
    var element = document.querySelector(element_id);
    element.style.display = 'inline-block';

}

// Gets an elemnt id and removes it from the page
function hideForm(element_id) {
    var element = document.querySelector(element_id);
    element.style.display = 'none';
}


// On Create btn click
option_create_btn.addEventListener('click', () => showForm('#create-task-form'));
// After submitted form can be removed
submit_create_btn.addEventListener('click', () => hideForm('#create-task-form'));

// On delete btn click
option_delete_btn.addEventListener('click', () => showForm('#delete-task-form'))
// After submitted form can be removed
submit_delete_btn.addEventListener('click', () => hideForm('#delete-task-form'))
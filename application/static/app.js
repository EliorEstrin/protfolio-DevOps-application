let card_with_sample_data = `
<div class="card mb-4">
<div class="card-header text-center h2">
  Learn neovim
</div>
<div class="card-body">
  <h5 class="card-title text-center h4">figure out how to create macros</h5>
  <p class="card-text text-center">Assigned To: <span class="font-weight-bold">My-self</span></p>
  <div class="d-grid gap-2 col-2 mx-auto">
  <a href="#" class="btn btn-primary">Edit</a>
  <a href="#" class="btn btn-danger">Delete</a>
</div>
</div>
</div>
  `;

let card_with_form = `
<div class="card col-sm-6 d-grid mb-5 mx-auto" style="width: 25rem; min-width:300px;">
<div class="card-body text-center h3">
  <div class="card-header text-center h2  bg-light">
    Create Task
  </div>
    <form>
      <div class="input-group mb-3 form-control-lg">
        <span class="input-group-text">Task Name</span>
        <input type="text" aria-label="Last name" class="form-control" name="input-taskName">
      </div>

      <div class="input-group mb-3 form-control-lg">
        <span class="input-group-text">Task Description</span>
        <input type="text" aria-label="Last name" class="form-control" name="input-description">
      </div>

      <div class="input-group form-control-lg  mb-3">
        <span class="input-group-text">Assinged To</span>
        <input type="text" aria-label="Last name" class="form-control" name="input-assingTo">
      </div>

      <div class="input-group mb-3 form-control-lg">
        <span class="input-group-text">Proority Level</span>
        <select class="form-select" id="inputGroupSelect01">
          <option value="1">Low</option>
          <option value="2">Medium</option>
          <option value="3">High</option>
        </select>
      </div>


        <button type="submit" id="submit-task" class="btn btn-primary">Submit</button>
    </form>
</div>
</div>
`;

// A reference to the create task button element in the DOM.
const create_task_btn = $("#create-task");

$(document).ready(function () {
  //loadTasks will render all tasks on page load
  loadTasks();

  // A click event listener for the create task button that appends the form for creating a task.
  create_task_btn.click(function () {
    $("#create-window").append(card_with_form);
  });

  /**
 * submit-task click event listener
 * 
 * @description A click event listener for the submit task button that submits the task creation form via an AJAX request to the server.
 * @event
 * 
 * 1. Prevent default form submit behavior
 * 2. Gather form data from the DOM
 * 3. Stringify the form data
 * 4. Make a POST request to the "/api/tasks" endpoint
 * 5. On success, call the loadTasks() function
 * 6. On error, log the error to the console
 */
  $(document).on("click", "#submit-task", function (e) {
    e.preventDefault();

    var form_taskName = $("input[name=input-taskName]").val();
    var form_description = $("input[name=input-description]").val();
    var form_assignedTo = $("input[name=input-assingTo]").val();
    var form_priority = $(".form-select").find(":selected").text();

    var formData = {
      taskName: form_taskName,
      description: form_description,
      assignedTo: form_assignedTo,
      priority: form_priority,
    };
    console.log(formData);

    // Send POST /api/tasks to create a task
    $.ajax({
      type: "POST",
      url: "/api/tasks",
      data: JSON.stringify(formData),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (result) {
        loadTasks();
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  });

  /**
 * loadTasks
 * 
 * @description A function that retrieves all tasks from the server and appends them to the main element in the DOM.
 * 
 * 1. Empties the main element in the DOM
 * 2. Makes a GET request to the "/api/tasks" endpoint
 * 3. On success, render each task
 * 4. On error, log the error to the console
 */
  function loadTasks() {
    //empty before loading if not already
    $("#main").empty();

    $.ajax({
      type: "GET",
      url: "/api/tasks",
      success: function (result) {
        console.log(result);
        // render the result
        result.forEach(function (result) {
          $("#main").append(
            create_task_to_render(
              result._id,
              result.taskName,
              result.description,
              result.priority,
              result.assignedTo
            )
          );
        });
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  }

  /**
 * delete button click event listener
 * 
 * @description A click event listener for the delete button that deletes a task from the server and reloads all tasks.
 * @event
 * 
 * 1. Retrieve the task ID from the closest parent card element
 * 2. Make a DELETE request to the "/api/tasks/{taskId}" endpoint
 * 3. On success, log a message to the console and call the loadTasks() function
 * 4. On error, log an error message to the console
 */
  $(document).on("click", ".delete", function () {
    var card = $(this).closest(".card");
    var taskId = card.attr("id");
    $.ajax({
      type: "DELETE",
      url: `/api/tasks/${taskId}`,
      success: function (response) {
        console.log("Task delete successfully");
        loadTasks();
        
      },
      error: function (error) {
        console.error("Error updating task:", error);
      },
    });
  });

  /**
 * Edit Task
 * 
 * Toggles the task card's editable mode on button click.
 * .closest is used to find the parent card to find the elements that need to be editibale  
 * Sends an HTTP PUT request to the server to update the task.
 * 
 * @event click on ".edit" button
 */
  $(document).on("click", ".edit", function () {
    var card = $(this).closest(".card");
    var taskId = card.attr("id");

    if ($(this).text() === "Confirm Changes") {
      var taskName = card.find(".card-header").text().trim();
      var description = card.find(".card-title").text();
      var assignedTo = card.find(".assinged-to").text();
      var priority = card.find(".task-priority").text();

      var taskData = {
        taskName: taskName,
        description: description,
        assignedTo: assignedTo,
        priority: priority,
      };
      console.log(taskData);

      $.ajax({
        type: "PUT",
        url: `/api/tasks/${taskId}`,
        data: JSON.stringify(taskData),
        contentType: "application/json",
        success: function (response) {
          console.log("Task updated successfully");
        },
        error: function (error) {
          console.error("Error updating task:", error);
        },
      });
    }

    card
      .find(".card-header, .card-title, .card-text span")
      .toggleClass("editable");
    card
      .find(".card-header, .card-title, .card-text span")
      .attr("contentEditable", function (_, attr) {
        return attr == "true" ? false : true;
      });
    card.find(".card-header").focus();
    $(this).text(function (i, text) {
      return text === "Edit" ? "Confirm Changes" : "Edit";
    });
  });
});

/**
 * create_task_to_render
 * 
 * This function is used to create the HTML string that represents a task to be rendered in the main div.
 * 
 * @param {string} task_id - The unique identifier for the task
 * @param {string} task_name - The name of the task
 * @param {string} task_description - The description of the task
 * @param {string} task_priority - The priority level of the task
 * @param {string} task_assinged_to - The person the task is assigned to
 * 
 * @return {string} - The HTML string representation of the task
 */
function create_task_to_render(
  task_id,
  task_name,
  task_description,
  task_priority,
  task_assinged_to
) {
  return `
  <div id="${task_id}" class="card mb-4">
  <div class="card-header text-center h2">
    ${task_name}
  </div>
  <div class="card-body">
    <h5 class="card-title text-center h4">${task_description}</h5>
    <p class="card-text text-center">Assigned To: <span class="assinged-to font-weight-bold">${task_assinged_to}</span></p>
    <p class="card-text text-center">Priority Level: <span class="task-priority font-weight-bold">${task_priority}</span></p>
    <div class="d-grid gap-2 col-2 mx-auto">
    <a class="btn btn-primary edit">Edit</a>
    <a class="btn btn-danger delete">Delete</a>
  </div>
  </div>
  </div>
  `;
}

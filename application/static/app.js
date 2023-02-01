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

// importand btns
const create_task_btn = $("#create-task");

$(document).ready(function () {
  //loadTasks will render all tasks on page load
  loadTasks();


  // When user creates a task generate a window
  create_task_btn.click(function () {
    $("#create-window").append(card_with_form);  
  });


  // Sumbit of a new task
  $(document).on("click", "#submit-task", function (e) {
    e.preventDefault(); // prevent the form from submitting normally

    var form_taskName = $("input[name=input-taskName]").val()
    var form_description = $("input[name=input-description]").val()
    var form_assignedTo = $("input[name=input-assingTo]").val()
    var form_priority = $('.form-select').find(":selected").text();
    
    var formData = {
      taskName: form_taskName,
      description: form_description,
      assignedTo: form_assignedTo,
      priority: form_priority,
    };    
    console.log(formData)

    // Send POST /api/tasks to create a task
    $.ajax({
      type: "POST",
      url: "/api/tasks",
      data: JSON.stringify(formData),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (result) {
        loadTasks()
        //reload the page on each change
        // location.reload();
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  });  

  //function to load all the task GET /api/tasks

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

  // Edit mode on the btn click
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
        success: function(response) {
          console.log("Task updated successfully");
        },
        error: function(error) {
          console.error("Error updating task:", error);
        }
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

// create_task_to_render is a function to make the task that will be rendered in the main div
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
    <a class="btn btn-danger">Delete</a>
  </div>
  </div>
  </div>
  `;
}

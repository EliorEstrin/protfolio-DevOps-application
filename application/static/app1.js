// Definitation of btn that acced later in the code
//Options
const option_create_btn = document.querySelector("#option_create");
const option_delete_btn = document.querySelector("#option_delete");
const option_edit_btn = document.querySelector("#option_edit");
const option_sort_btn = document.querySelector("#option_sort");

//Sumbit btn
const submit_create_btn = document.querySelector("#create_task_btn");
const submit_delete_btn = document.querySelector("#delete_task_btn");
const submit_edit_btn = document.querySelector("#edit_task_btn");
const submit_sort_btn = document.querySelector("#sort_task_btn");

// by deafult:
hideAll();

// Funtion to hide all form elements that created afer a btn is pressed
// Usefull when the page reload after a form get submitted
function hideAll() {
  hideForm("#create-task-form");
  hideForm("#delete-task-form");
  hideForm("#edit-task-form");
  hideForm("#sort-task-form");
}

// gets an element and shows him on the page
function showForm(element_id) {
  hideAll();
  var element = document.querySelector(element_id);
  element.style.display = "inline-block";
}

// Gets an elemnt id and removes it from the page
function hideForm(element_id) {
  var element = document.querySelector(element_id);
  element.style.display = "none";
}

// On Create btn click
option_create_btn.addEventListener("click", () =>
  showForm("#create-task-form")
);
// After submitted form can be removed
submit_create_btn.addEventListener("click", () =>
  hideForm("#create-task-form")
);

// On delete btn click
option_delete_btn.addEventListener("click", () =>
  showForm("#delete-task-form")
);
// After submitted form can be removed
submit_delete_btn.addEventListener("click", () =>
  hideForm("#delete-task-form")
);

// On edit btn click
option_edit_btn.addEventListener("click", () => showForm("#edit-task-form"));
//After submitted get beremoved
submit_edit_btn.addEventListener("click", () => hideForm("#edit-task-form"));

// On sort btn click
option_sort_btn.addEventListener("click", () => showForm("#sort-task-form"));
//After submitted get beremoved
submit_sort_btn.addEventListener("click", () => hideForm("#sort-task-form"));

// Using Jquery from here to fetch responses
$(document).ready(function () {
  // Create new task
  $("#create-form").submit(function (e) {
    e.preventDefault(); // prevent the form from submitting normally
    var formData = {
      taskName: $("input[name=task_name]").val(),
      description: $("input[name=description]").val(),
      assignedTo: $("input[name=assigned_to]").val(),
      priority: $("input[name=priority_level]").val(),
    };

    $.ajax({
      type: "POST",
      url: "/api/tasks",
      data: JSON.stringify(formData),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (result) {
        // loadTasks()
        //reload the page on each change
        location.reload();
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  });

  // Delete task
  $("#delete-form").submit(function (event) {
    event.preventDefault();
    var task_name = $("input[name=task_id]").val();
    $.ajax({
      type: "DELETE",
      url: "/api/tasks/" + task_name,
      success: function (result) {
        location.reload();
      },
      error: function (xhr, status, error) {
        alert("Item Not Found");
        console.log(error);
      },
    });
  });

  //Update Task
  $("#update-form").submit(function (e) {
    e.preventDefault(); // prevent the form from submitting normally
    var task_id = $("input[name=task_id_to_edit]").val();
    var formData = {
      description: $("input[name=description_edit]").val(),
    };
    $.ajax({
      type: "PUT",
      url: "/api/tasks/" + task_id,
      data: JSON.stringify(formData),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function (result) {
        //reload the page on each change
        location.reload();
      },
      error: function (xhr, status, error) {
        alert("ID Not Found");
      },
    });
  });

  //Sort tasks By status
  $("#sort-form").submit(function (e) {
    e.preventDefault(); // prevent the form from submitting normally
    var task_status = $("input[name=task_status_sort]").val();
    console.log(task_status);
    $.ajax({
      type: "GET",
      url: "/api/tasks/" + task_status,
      success: function (result) {
        $("tbody").empty();
        result.forEach(function (result) {
            $("tbody").append(
                "<tr>" +
                  "<td>" +
                  result._id +
                  "</td>" +
                  "<td>" +
                  result.taskName +
                  "</td>" +
                  "<td>" +
                  result.description +
                  "</td>" +
                  "<td>" +
                  result.assignedTo +
                  "</td>" +
                  "<td>" +
                  result.priority +
                  "</td>" +
                  "</tr>"
              );
          });
        
      },
      error: function (xhr, status, error) {
        console.log(error);
        alert(2);
      },
    });
  });

  //Get all tasks
  function loadTasks() {
    // make the AJAX call
    $.ajax({
      type: "GET",
      url: "/api/tasks",
      success: function (result) {
        // handle the result here
        // you can update the page with the result or display a message
        result.forEach(function (result) {
          $("tbody").append(
            "<tr>" +
              "<td>" +
              result._id +
              "</td>" +
              "<td>" +
              result.taskName +
              "</td>" +
              "<td>" +
              result.description +
              "</td>" +
              "<td>" +
              result.assignedTo +
              "</td>" +
              "<td>" +
              result.priority +
              "</td>" +
              "</tr>"
          );
        });
      },
      error: function (xhr, status, error) {
        console.log(error);
      },
    });
  }

  loadTasks();
});

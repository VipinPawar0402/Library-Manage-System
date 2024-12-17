$(document).ready(function () {
    $("button.deletebtn").click(function () {
      var id = $(this).data("id");
      $.get("/delete/" + id + "/", function (response) {
        $("#item-" + id).remove();
        alert("data is deleted");
      });
    });
  });

  // function edit_data(){
  //   $('#exampleModal').modal('show');
  // }

  function open_modal(id, name, mobile, email) {
    $("#exampleModal").modal("show");
    // Populate modal fields with fetched data
    $("#editname").val(name);
    $("#editmobile").val(mobile);
    $("#editemail").val(email);
    $("#userId").val(id);
  }

  function update_data() {
    var name = $("#editname").val();
    var mobile = $("#editmobile").val();
    var email = $("#editemail").val();
    var id = $("#userId").val();

    console.log("Name:", name);
    console.log("Mobile:", mobile);
    console.log("Email:", email);
    console.log("ID:", id);

    $.ajax({
      method: "POST",
      url: "/update-person/",
      data: {
        name: name,
        email: email,
        mobile: mobile,
        id: id,
        // csrfmiddlewaretoken: "{{ csrf_token }}", // CSRF token
      },
      success: function (response) {
        if (response.message === "success") {
          alert("Data updated successfully!");
          window.location.href = "/persondata/";
        } else {
          alert("Failed to update data.");
        }
      },
      error: function () {
        alert("An error occurred while updating the data.");
      },
    });
  }
document.getElementById("createStudent").addEventListener("click", function() {
    // Show the input fields
    document.getElementById("studentInputFields").style.display = "block";
});

document.getElementById("confirmCreateStudent").addEventListener("click", function() {
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;

    // Simple validation
    if(firstName.trim() === "" || lastName.trim() === "") {
        alert("Please enter both first and last names.");
        return;
    }

    // Send data to server
    $.post("/createStudent", { name: firstName, last_name: lastName }, function(response) {
        // Hide the input fields and clear them
        document.getElementById("studentInputFields").style.display = "none";
        document.getElementById("firstName").value = "";
        document.getElementById("lastName").value = "";

        // Update the class list
        makeClassList();
    });
});

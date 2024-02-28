document.getElementById("createStudent").addEventListener("click", function() {
    // Show the input fields
    document.getElementById("studentInputFields").style.display = "block";
});

/*document.getElementById("confirmCreateStudent").addEventListener("click", function() {
    var first_Name = document.getElementById("first_Name").value;
    var last_Name = document.getElementById("last_Name").value;

    // Simple validation
    if(first_Name.trim() === "" || last_Name.trim() === "") {
        alert("Please enter both first and last names.");
        return;
    }

    // Send data to server
    $.post("/createStudent", { first_name: first_Name, last_name: last_Name }, function(response) {
        // Hide the input fields and clear them
        document.getElementById("studentInputFields").style.display = "none";
        document.getElementById("first_Name").value = "";
        document.getElementById("last_Name").value = "";

        // Update the class list
        makeClassList();
    });
});*/
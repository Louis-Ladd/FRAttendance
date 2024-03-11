var createStudentButton = document.getElementById("createStudent");
var inputFirstname = document.getElementById("first_name");
var inputLastname = document.getElementById("last_name");
if (createStudentButton) {
    createStudentButton.addEventListener("click", function() {
        // Show the input fields
        var studentInputFields = document.getElementById("studentInputFields");
        if (studentInputFields) {
            studentInputFields.style.display = "block";
        }

        // Send a POST request to the createStudent endpoint
        fetch('/database/createStudent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                first_name: inputFirstname.value, // Replace with the actual first name input value
                last_name: inputLastname.value // Replace with the actual last name input value
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to create student');
            }
        })
        .then(data => {
            // Handle the response data as needed
            console.log('Student created:', data);
        })
        .catch(error => {
            // Handle any errors
            console.error('Error creating student:', error);
        });
    });
}


function loadStudents(className) {
    fetch(`/database/getClass/${className}`)
        .then(response => response.json())
        .then(data => {
            const studentContainer = document.getElementById('studentContainer');
            studentContainer.innerHTML = ''; // Clear existing student boxes

            const studentBoxTemplate = document.getElementById('studentBoxTemplate');

            data.forEach(student => {   
                const studentBox = studentBoxTemplate.content.cloneNode(true);
                studentBox.querySelector('.StudentName').textContent = `${student[0]} ${student[1]}`;
                studentBox.querySelector('.StudentTardies').textContent = `Tardies: ${student[4]}`;
                studentContainer.appendChild(studentBox); 
                               
            });
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    // Fetch classes using user.getClasses API call in Python
    fetch('/users/getClasses')
        .then(response => response.json())
        .then(data => {
            const classDropdown = document.getElementById('classDropdown');
            data.forEach(className => { // Assuming data is an array of classes
                const option = document.createElement('option');
                option.value = className;
                option.textContent = className;
                classDropdown.appendChild(option);
            });

            if (classDropdown.options.length > 0) {
                loadStudents(classDropdown.options[0].value); // Load students for the first class
            }
        });
});


document.addEventListener("DOMContentLoaded", function() {
    const classDropdown = document.getElementById('classDropdown');
    const studentDropdown = document.getElementById('studentDropdown');

    // Fetch classes using user.getClasses API call in Python
    fetch('/dashboard')
        .then(response => response.json())
        .then(data => {
            data.classes.forEach(className => {
                const option = document.createElement('option');
                option.value = className;
                option.textContent = className;
                classDropdown.appendChild(option);
            });

            if (classDropdown.options.length > 0) {
                loadStudents(classDropdown.options[0].value);
            }
        });

    // Add event listener to the class dropdown
    classDropdown.addEventListener('change', function() {
        loadStudents(classDropdown.value);
    });

    // Load the first student in the dropdown box automatically
    if (classDropdown.options.length > 0) {
        loadStudents(classDropdown.options[0].value);
    }
});
var createStudentButton = document.getElementById("createStudent");
var confirmStudentButton = document.getElementById("confirmCreateStudent");
var inputFirstname = document.getElementById("first_name");
var inputLastname = document.getElementById("last_name");
var classDropdown = document.getElementById("classDropdown");

if (createStudentButton) {
    createStudentButton.addEventListener("click", function() {
        var studentInputFields = document.getElementById("studentInputFields");
        if (studentInputFields) {
            studentInputFields.style.display = "block";
        }
        console.log('Create student button clicked');
    });

    confirmStudentButton.addEventListener("click", function() {
        // Get the selected class from the dropdown menu
        var selectedClass = classDropdown.options[classDropdown.selectedIndex].value;
    
        fetch('/database/createStudent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                first_name: inputFirstname.value,
                last_name: inputLastname.value,
                selected_class: selectedClass // Include the selected class in the request body
            })
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                return response.text(); // Return the text response
            }
        })
        .then(data => {
            if (typeof data === 'string') {
                console.log('Non-JSON response:', data);
                // Handle the non-JSON response here
            } else {
                // Handle the JSON response as needed
                console.log('Student created:', data);
            }
        })
        .catch(error => {
            // Handle any errors
            console.error('Error creating student:', error);
        });
    });
}


function loadStudents(className) {
    console.log('Loading students for class:', className);

    // Check if the className is the placeholder "select a class"
    if (className === "select_a_class") {
        console.log('Class name is the placeholder "select a class". Finding the first populated class instead.');
        // If the className is the placeholder, load the first populated class instead
        var classDropdown = document.getElementById("classDropdown");
        for (var i = 0; i < classDropdown.options.length; i++) {
            if (classDropdown.options[i].value !== "select_a_class") {
                className = classDropdown.options[i].value;
                console.log('Found populated class:', className);
                break;
            }
        }
    }

    console.log('Fetching data for class:', className);
    fetch(`/database/getClass/${className}`)
        .then(response => response.json())
        .then(data => {
            console.log('Received data for class:', className, data);
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
        .catch(error => console.error('Error fetching data for class:', className, error));
}

document.addEventListener("DOMContentLoaded", function() {
    // Fetch classes using user.getClasses API call in Python
    fetch('/user/getClasses')
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
var createStudentButton = document.getElementById("createStudent");
if (createStudentButton) {
    createStudentButton.addEventListener("click", function() {
        // Show the input fields
        var studentInputFields = document.getElementById("studentInputFields");
        if (studentInputFields) {
            studentInputFields.style.display = "block";
        }
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
    fetch('/dashboard')
        .then(response => response.json())
        .then(data => {
            const classDropdown = document.getElementById('classDropdown');
            data.classes.forEach(className => {
                const option = document.createElement('option');
                option.value = className;
                option.textContent = className;
                classDropdown.appendChild(option);
            });
        });
});


document.addEventListener("DOMContentLoaded", function() {
    fetch('/dashboard')
        .then(response => response.json())
        .then(data => {
            const classDropdown = document.getElementById('classDropdown');
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
});
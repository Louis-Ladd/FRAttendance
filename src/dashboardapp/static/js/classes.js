document.getElementById("createStudent").addEventListener("click", function() {
    // Show the input fields
    document.getElementById("studentInputFields").style.display = "block";
});


function loadStudents(className) {
    fetch(`/getClass/${className}`)
        .then(response => response.json())
        .then(data => {
            const studentContainer = document.getElementById('studentContainer');
            studentContainer.innerHTML = ''; // Clear existing student boxes

            data.forEach(student => {
                const studentBox = document.createElement('div');
                studentBox.className = 'student-box';
                studentBox.textContent = `${student.first_name} ${student.last_name}`; // Adjust based on your data structure
                studentContainer.appendChild(studentBox);
            });
        })
        .catch(error => console.error('Error:', error));
}

// Example usage
loadStudents("cyber"); // Replace "Math101" with the class name you want to load

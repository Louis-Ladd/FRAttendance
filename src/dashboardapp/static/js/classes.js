document.getElementById("createStudent").addEventListener("click", function() {
    // Show the input fields
    document.getElementById("studentInputFields").style.display = "block";
});


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

loadStudents("cyber"); // Replace "Math101" with the class name you want to load

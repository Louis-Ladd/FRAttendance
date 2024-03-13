const classListSelect = document.getElementById("classListDropdown");
const classListSortby = document.getElementById("classListSortby");

function tabSwitch(id){
    const filters = document.getElementById("filters");

    for (const child of filters.children){
        if (child.id == id) {
            child.classList.remove("unfilled-button");
            child.classList.add("filled-button");
        }
        else {
            child.classList.remove("filled-button");
            child.classList.add("unfilled-button");
        }
    }
    
    const overviews = document.getElementById("overviews-parent");
    
    for (const child of overviews.children){
        child.classList.remove("active");
        child.classList.add("inactive");
    }

    overviews.children[id].classList.remove("inactive");
    overviews.children[id].classList.add("active");

    //TODO: Validate this code please, this feels wrong... it is js tho - Louis
}

function makeClassList(className) {
    if (className == "") {
        const classList = document.getElementById("classList");
        classList.innerHTML = "";
        let placeholderElement = document.createElement("ul");
        let item = document.createElement("li");
        let text = document.createElement("h3");
        text.innerHTML = "You currently don't have any classes to view :(";
        item.appendChild(text);
        placeholderElement.appendChild(item);
        classList.appendChild(placeholderElement);
        return
    }
    $.get(`/database/getClass/${className}/20`, function(data){
        makeClassListFromData(data);
    });
}

// Yippee, building element from scratch - Louis
function makeClassListFromData(data) {
    document.getElementById("classList").innerHTML = "";
    let studentElement = document.createElement("ul");

    switch (document.getElementById("classListSortby").value) {
        case "0"://sort by tardies Acc
            data = data.sort(function (a, b) { return a[4] - b[4]; });
            break;
        case "1"://sort by tardies Dec
            data = data.sort(function (a, b) { return b[4] - a[4]; });
            break;    
        case "2"://sort by last name A to Z
            data = data.sort(function (a,b) {
                return a[1].localeCompare(b[1]);
            });
            break;
        case "3"://sort by last name Z to A
            data = data.sort (function (a,b) {
                return b[1].localeCompare(a[1]);
            })
            break;
    }
    
    for (var i = 0; i < data.length; i++){
        let item = document.createElement("li");
        let textDiv = document.createElement("div");
        let image = document.createElement("img")
        let name = document.createElement("h3");
        name.textContent = data[i][0] + " ";
        name.textContent += data[i][1];
        image.src = "static/media/avatar.jpg"
        textDiv.appendChild(image)
        textDiv.appendChild(name);
        textDiv.appendChild(document.createElement("br"));
        textDiv.appendChild(document.createTextNode("Tardies: " + data[i][4]));
        item.appendChild(textDiv);
        studentElement.appendChild(item);
        if (i != data.length-1) {
            studentElement.appendChild(document.createElement("hr"));
        }
    }
    document.getElementById("classList").appendChild(studentElement)
}

$.get("/user/getClasses", function(data){
    for (var i = 0; i < data.length; i++){
        classListSelect.innerHTML += "<option value=" + data[i] + ">" + data[i] + "</option>";
    }
    makeClassList(classListSelect.value);
})


classListSelect.addEventListener("change", function() {
    makeClassList(classListSelect.value);
})
classListSortby.addEventListener("change", function() {
    makeClassList(classListSelect.value);
})
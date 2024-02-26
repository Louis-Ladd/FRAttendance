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

function makeClassList() {
    document.getElementById("classListTitle").innerHTML = "Cyber"
    $.get("/getClass/cyber", function(data){
        makeClassListFromData(data);
    });
}

function makeClassListFromData(data) {
    var studentElement = document.createElement("ul");
    for (var i = 0; i < data.length; i++){
        var item = document.createElement("li");
        var textDiv = document.createElement("div");
        var image = document.createElement("img")
        image.src = "static/media/avatar.jpg"
        textDiv.appendChild(image)
        textDiv.appendChild(document.createTextNode(data[i][0] + " "));
        textDiv.appendChild(document.createTextNode(data[i][1]));
        textDiv.appendChild(document.createElement("br"));
        textDiv.appendChild(document.createTextNode("Tardies: " + data[i][4]));
        item.appendChild(textDiv);
        studentElement.appendChild(item);
    }
    document.getElementById("classList").appendChild(studentElement)
}
//document.getElementById("classList").appendChild(makeClassList())
makeClassList()
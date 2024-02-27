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

String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{([0-9]+)}/g, function (match, index) {
        return typeof args[index] == 'undefined' ? match : args[index];
    });
};

function makeClassList(className) {
    document.getElementById("classListTitle").innerHTML = className
    $.get('/getClass/{0}/20'.format(className), function(data){
        makeClassListFromData(data);
    });
}

// Yippee, building element from scratch - Louis
function makeClassListFromData(data) {
    var studentElement = document.createElement("ul");
    for (var i = 0; i < data.length; i++){
        var item = document.createElement("li");
        var textDiv = document.createElement("div");
        var image = document.createElement("img")
        var name = document.createElement("h3");
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
//document.getElementById("classList").appendChild(makeClassList())
makeClassList("vr")
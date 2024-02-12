function pageSwitch(page, id, isNested) {
    var parentDocument = isNested ? window.parent.document : document;

    parentDocument.getElementById("content-iframe").src = page;
    buttons = parentDocument.getElementsByClassName("navbar-button");
    for (let i = 0; i < buttons.length; i++){
        buttons[i].classList.remove("active")
    }
    parentDocument.getElementById(id).getElementsByTagName("i")[0].classList.add("active")
}
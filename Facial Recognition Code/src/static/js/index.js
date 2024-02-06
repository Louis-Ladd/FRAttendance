var navbarButtons = document.querySelectorAll(".navbar-buttons")

function cameraSwitch(page, id) {
    document.getElementById("content-iframe").src = page;
    buttons = document.getElementsByClassName("navbar-button");
    for (let i = 0; i < buttons.length; i++){
        buttons[i].classList.remove("active")
    }
    document.getElementById(id).getElementsByTagName("i")[0].classList.add("active")
}
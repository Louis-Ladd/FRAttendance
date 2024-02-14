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
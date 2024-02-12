var socket = io();
const dynamic_element_ids = ["ip","cpu_usage", "ram_usage"]

socket.on("connect", function() {
    socket.emit("data", {data: "I\'m connected!"});
});

socket.on("info_update", function(data) {
    for (var i = 0; i < dynamic_element_ids.length; i++){
        if (Array.isArray(data[dynamic_element_ids[i]])){
            document.getElementById(dynamic_element_ids[i]).innerText = data[dynamic_element_ids[i]][data[dynamic_element_ids[i]].length-1];
        }
        else{
            document.getElementById(dynamic_element_ids[i]).innerText = data[dynamic_element_ids[i]];
        }
    }
    socket.emit("refresh");
})



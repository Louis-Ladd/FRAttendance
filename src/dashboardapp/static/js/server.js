var socket = io();
var cpu_usage_history = [];
const dynamic_element_ids = ["ip","cpu_usage", "ram_usage"];

var cpu_chart = new Chart(document.getElementById("cpu_usage_graph"), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'CPU Usage %',
            data: [],
            borderWidth: 1
        }]
    },
    options: {
        elements: {
            point: {
                radius: 0
            }
        },
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

function addData(chart, label, newData) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(newData);
    });
    chart.update();
}

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
    addData(cpu_chart, "", data["cpu_usage"][data["cpu_usage"].length-1])
    if (cpu_chart.data.datasets[0].data.length > 100) {
        //TODO: remove first datapoints
    }
    socket.emit("refresh");
})



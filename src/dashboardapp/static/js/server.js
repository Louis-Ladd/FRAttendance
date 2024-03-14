/*
 * File: server.js
 * Purpose: Handle instatiation of chart.js and socket.io to handle server statistics in server.html
 * Project: FRAttendance
 * File Created: Thursday, 14th March 2024 12:25:28 pm
 * Author: Louis Harshman (lewisharshman1@gmail.com)
 * -----
 * Last Modified: Thursday, 14th March 2024 3:41:56 pm
 * Modified By: Louis Harshman (lewisharshman1@gmail.com)
 * -----
 * Copyright 2019 - 2024 
 */

var socket = io();
var cpu_usage_history = [];
var lastGraphUpdate = Date.now()
const dynamic_element_ids = ["ip","cpu_usage", "ram_usage"];
const formatter = new Intl.DateTimeFormat('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });

var options = {
    elements: {
        point: {
            radius: 0
        }
    },
    scales: {
        x:{
            grid: {
                display: false
            }
        },
        y: {
            max: 100,
            beginAtZero: true
        }
    }
}


//TODO: compact graph institiation code - Louis
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
    options
});

var memory_chart = new Chart(document.getElementById("memory_usage_graph"), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Memory Usage %',
            data: [],
            borderWidth: 1
        }]
    },
    options
});

function addData(chart, label, newData){
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(newData);
    });
    chart.update();
}

socket.on("connect", function() {
    socket.emit("data", {data: "I\'m connected!"});
});

socket.on("info_update", function(data){
    const currentDate = new Date();
    var currentTime = currentDate.toLocaleString('en-US', { hour: 'numeric', minute: "numeric", second: "numeric", hour12: false });
    for (var i = 0; i < dynamic_element_ids.length; i++){
        if (Array.isArray(data[dynamic_element_ids[i]])){
            document.getElementById(dynamic_element_ids[i]).innerText = data[dynamic_element_ids[i]][data[dynamic_element_ids[i]].length-1];
        }
        else{
            document.getElementById(dynamic_element_ids[i]).innerText = data[dynamic_element_ids[i]];
        }
    }

    //TODO: Make this code less verbose - Louis
    if ((Date.now() - lastGraphUpdate) > 500){
        addData(cpu_chart, currentTime, data["cpu_usage"][data["cpu_usage"].length-1]);
        addData(memory_chart, currentTime, data["ram_usage"][data["ram_usage"].length-1]);
        lastGraphUpdate = Date.now();
    }

    if (cpu_chart.data.datasets[0].data.length > 100) {
        cpu_chart.data.labels.shift();
        cpu_chart.data.datasets[0].data.shift();
    }
    if (memory_chart.data.datasets[0].data.length > 100) {
        memory_chart.data.labels.shift();
        memory_chart.data.datasets[0].data.shift();
    }
    socket.emit("refresh");
})



/*
 * File: accounts.js
 * Purpose: Handle creating the user list and handling user input from accounts.html
 * Project: FRAttendance
 * File Created: Thursday, 14th March 2024 12:25:28 pm
 * Author: Louis Harshman (lewisharshman1@gmail.com)
 * -----
 * Last Modified: Thursday, 14th March 2024 3:41:21 pm
 * Modified By: Louis Harshman (lewisharshman1@gmail.com)
 * -----
 * Copyright 2019 - 2024 
 */

function makeUserList() {
    var userList = document.getElementById("accountsContainer");
    userList.innerHTML = "";
    let currentUser = "";
    getCurrentUser().then (function(username) {
        currentUser = username
    });

    fetch("/users/getUsers")
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            let userListElement = document.createElement("ul");
            for (var i = 0; i < data["username"].length; i++) {
                let userElement = document.createElement("li");
                let userInfoDiv = document.createElement("div");
                let name = document.createElement("h3");
                let username = document.createElement("p");
                let classes = document.createElement("p");

                name.innerHTML = data["name"][i] + "  ";
                username.innerHTML = `Username: ${data["username"][i]}`;
                userElement.appendChild(name);

                if (data["isAdmin"][i]) {
                    let adminIcon = document.createElement("i");
                    let adminText = document.createElement("span");
                    adminText.innerHTML = "Admin";
                    adminIcon.classList.add("fa", "fa-shield-halved");
                    adminIcon.innerHTML = " ";
                    adminIcon.appendChild(adminText);
                    name.appendChild(adminIcon);   
                }

                classes.innerHTML = "Classes: ";
                for (var j = 0; j < data["classes"][i].length; j++) {
                    classes.innerHTML += `${data["classes"][i][j]} `;
                }

                userInfoDiv.appendChild(classes);
                userInfoDiv.appendChild(username);
                userElement.appendChild(userInfoDiv);
                if (data["username"][i] !== currentUser) {
                    userElement.appendChild(makeDeleteUserButton(data["username"][i]));
                }
                userListElement.appendChild(userElement);
            }
            userList.appendChild(userListElement);
        });
}

function getCurrentUser() {
    return fetch("/user/getUsername")
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            return data["username"];
        })
        .catch(function(error) {
            console.error("Could not fetch username",error);
            return "";
        });
}

function deleteUser(username) {
    fetch("/users/deleteUser", {
        method: "POST",
        headers : {
            "Content-Type": "application/json"
        },
        body : JSON.stringify({
            username: username
        })
    });
    makeUserList();
}

function makeDeleteUserButton(username) {
    var button = document.createElement("button");
    var deleteIcon = document.createElement("i");
    deleteIcon.classList.add("fa", "fa-trash-can");
    button.innerHTML = "Delete";
    button.classList.add("filled-button");
    button.appendChild(deleteIcon);
    button.onclick = function() {deleteUser(username)};
    return button;
}
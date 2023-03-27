/**
 * Fonction qui permet la recherche d'utilisateur parmi une liste.
 */
function search() {
    const searchBarValue = document.getElementById("search").value.toUpperCase();
    const tableau        = document.getElementById("user-list");

    var lines = tableau.getElementsByTagName("tr");

    for (i = 0; i < lines.length; i++) {
        user_id = lines[i].getElementsByTagName("td")[0];

        if(user_id) {
            texte = user_id.innerText;

            if (texte.toUpperCase().indexOf(searchBarValue) > -1) {
                lines[i].style.display = "";
            }
            else {
                lines[i].style.display = "none";
            }
        }
    }
}        

/**
 * 
 */
document.getElementById("submit").addEventListener("click", () => {
    const alertValue = document.getElementById("select-right").value;
    const userValue  = document.getElementById("user").value;
    
    fetch("/supervisor_panel/assign_alert", {
        method: "POST",

        body: JSON.stringify({
            "user": {
                "user_id_connect": userValue
            },
            "alert": {
                "alert_name": alertValue
            }   
        }),

        headers: {
            "accept": "application/json",
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        console.log(response);
    }).catch(error => {
        console.log(error);
    });

    document.getElementById("user").value = "";

    var table = document.getElementById("user-list");
    var line  = table.insertRow(-1);
    var cel1  = line.insertCell(-1);
    var cel2  = line.insertCell(-1);
    var cel3  = line.insertCell(-1);
    var cel4  = line.insertCell(-1);

    cel1.innerText = userValue;
    cel2.innerText = new Date().toISOString();
    cel3.innerText = alertValue;
    cel4.innerHTML = `
    <button>\
        <span onclick="delete_user_alert(this, '{{`+ userValue +`}}', '{{`+ alertValue +`}}')">CONFIRM DELETE</span>\
        <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">\
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />\
        </svg>\
    </button>`;
});

/**
 * 
 */
function delete_user_alert(elt, user, alert) {
    fetch("/supervisor_panel/assign_alert", {
        method: "DELETE",

        body: JSON.stringify({
            "user": {
                "user_id_connect": user
            },
            "alert": {
                "alert_name": alert
            }
        }),

        headers: {
            "accept": "application/json",
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        console.log(response);
        elt.parentNode.parentNode.parentNode.style.display = "none";
    }).catch(error => {
        console.log(error);
    });
}
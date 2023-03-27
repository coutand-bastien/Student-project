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
 // # TODO: CSRF mettre en place
function update_authorization(select_obj, user_id_connect) {
    fetch("/admin_panel/rights_management", {
        method: "POST",

        body: JSON.stringify({
            user_id_connect: user_id_connect,
            authorization: select_obj.value
        }),

        headers: {
            "accept": "application/json",
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        response.json().then(data => console.log(data))
    });
}
        
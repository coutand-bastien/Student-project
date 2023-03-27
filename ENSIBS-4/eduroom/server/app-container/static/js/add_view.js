/**
 * 
 */
 // # TODO: CSRF mettre en place
 document.getElementById("confirm_add_ics").addEventListener("click", () => {
    let icsFile = document.getElementById("add_ics_input_file");
    let formData = new Formfetch("/admin_panel/add_view/create_room", {
        method: "POST",

        body: JSON.stringify({
            room: roomValue,
            nbr_place: nbrPlaceRoomValue
        }),

        headers: {
            "accept": "application/json",
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        response.json().then(data => console.log(data))
    });Data();
    formData.append('ics_file', icsFile.files[0]);

    fetch("/admin_panel/add_view/add_ics", {
        method: "POST",

        body: formData
    })
    .then(response => {
        response.json().then(data => console.log(data))
    });
});

/**
 * 
 */
 // # TODO: CSRF mettre en place
 document.getElementById("confirm_add_room").addEventListener("click", () => {
    const roomValue         = document.getElementById("add_room_input_text").value;
    const nbrPlaceRoomValue = document.getElementById("add_room_input_number").value;
    console.log(roomValue);
    console.log(nbrPlaceRoomValue);
    fetch("/admin_panel/add_view/create_room", {
        method: "POST",

        body: JSON.stringify({
            room: roomValue,
            nbr_place: nbrPlaceRoomValue
        }),

        headers: {
            "accept": "application/json",
            "Content-Type": "application/json",
        },
    })
    .then(response => {
        response.json().then(data => console.log(data))
    });
});
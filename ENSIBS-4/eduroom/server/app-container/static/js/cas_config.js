/**
 * When submit
 */
 // # TODO: CSRF mettre en place
let submit_btn = document.querySelector("send");

function update_cas() {
    const add  = document.getElementById("addresse").value;
    const port = document.getElementById("port").value;

    if (!add || !port) 
        alert("The value can not be empty !");

    const options = {
        method: 'POST',
      
        headers: {
            'Accept': 'text/html',
            'Content-Type': 'application/json'
        },
      
        body: JSON.stringify({
            cas_ip: add,
            cas_port: port
        })
    }

    fetch('http://127.0.0.1:8000/admin_panel/cas_config', options)
        .then(response => response.json()
                                  .then(data => {
                                        console.log(data);
                                    }));
}
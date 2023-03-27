// Sidebar Toggle Codes

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");
var sidebarCloseIcon = document.getElementById("sidebarIcon");

function toggleSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add("sidebar_responsive");
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove("sidebar_responsive");
    sidebarOpen = false;
  }
}

function show_value2(x)
{
  document.getElementById("slider_value2").innerHTML=x;

  fetch("/supervisor_panel/assign_alert/alert_rate", {
    method: "POST",

    body: JSON.stringify({
      "alert_rate": x
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
}

function add_one()
{
  document.getElementById("slider_input").value=(parseInt(document.getElementById("slider_input").value)+1);
  show_value2(document.getElementById("slider_input").value);
}

function subtract_one()
{
  document.getElementById("slider_input").value=parseInt(document.getElementById("slider_input").value)-1;
  show_value2(document.getElementById("slider_input").value);
}
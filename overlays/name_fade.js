let name_plate = document.getElementById("name_box");
let transition_time = 2500;

window.addEventListener("load", function(){
    setTimeout(function(){
            name_plate.setAttribute("class", "in");
    }, transition_time)
    setTimeout(function(){
        name_plate.setAttribute("class", "");
    }, transition_time*3);
  });
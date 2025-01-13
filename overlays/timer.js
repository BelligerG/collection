let timer = document.getElementById("timer");
let countdownDate = new Date().getTime() + 15*60000;

let t = setInterval(() => {
    let now = new Date().getTime()

    let distance = countdownDate - now;

    let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((distance % (1000 * 60)) / 1000);

    timer.innerHTML = minutes.toString().padStart(2, '0') + ": " + seconds.toString().padStart(2, '0');

    if (distance<0){
        clearInterval(t);
        timer.innerHTML = "Soon!";
    }
}, 1000);
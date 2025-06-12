let current = 1;
const total = 5;
console.log("asdasidnaosndoansdkjansdk")
function autoSlideCarousel() {
    document.getElementById(`carousel${current}`).checked = true;
    current = current % total + 1;
}

setInterval(autoSlideCarousel, 3000);

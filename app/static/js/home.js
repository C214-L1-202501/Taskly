let current = 1;
const total = 5;

function autoSlideCarousel() {
    document.getElementById(`carousel${current}`).checked = true;
    current++;
    if (current > total) {
        current = 1;
    }
}

setInterval(autoSlideCarousel, 3000);

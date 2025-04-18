let current = 1;
const total = 5;
let direction = 1;

function autoSlideCarousel() {
    document.getElementById(`carousel${current}`).checked = true;

    current += direction;

    if (current > total) {
        current = total - 1;
        direction = -1;
    } else if (current < 1) {
        current = 2;
        direction = 1;
    }
}

setInterval(autoSlideCarousel, 3000);

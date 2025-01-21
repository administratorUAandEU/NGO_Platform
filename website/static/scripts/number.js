function animateNumber(target, duration, easingFunction) {
    const start = 0;
    const end = target;
    const element = document.getElementById("number");

    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;

        const progress = Math.min(elapsed / duration, 1);

        const easedProgress = easingFunction(progress);

        const currentValue = Math.round(start + (end - start) * easedProgress);

        element.textContent = currentValue;

        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

function easeInOutQuad(t) {
    return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
}

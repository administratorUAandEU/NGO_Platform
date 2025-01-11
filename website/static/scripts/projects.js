document.addEventListener("DOMContentLoaded", () => {
    const toggleButtons = document.querySelectorAll(".toggle-btn");

    document.querySelectorAll(".card-text").forEach(cardText => {
        const button = cardText.nextElementSibling;
        if (cardText.scrollHeight <= 80) {
            button.style.display = "none";
        }
    });

    toggleButtons.forEach(button => {
        button.addEventListener("click", () => {
            const targetId = button.getAttribute("data-target");
            const target = document.getElementById(targetId);

            if (target.classList.contains("card-text-hidden")) {
                target.style.maxHeight = target.scrollHeight + "px";
                target.classList.remove("card-text-hidden");
                target.classList.add("card-text-visible");
                button.textContent = "Show Less";

                target.addEventListener(
                    "transitionend",
                    () => {
                        target.style.maxHeight = null;
                    },
                    { once: true }
                );
            } else {
                target.style.maxHeight = target.scrollHeight + "px";
                requestAnimationFrame(() => {
                    target.style.maxHeight = "80px";
                });

                target.classList.remove("card-text-visible");
                target.classList.add("card-text-hidden");
                button.textContent = "Read More";
            }
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {
    // Function to filter news cards based on selected tags
    function filterNews() {
        var selectedTags = Array.from(document.querySelectorAll('.form-check-input:checked'))
            .map(checkbox => checkbox.value);
        var newsCards = document.querySelectorAll('.news-card');

        newsCards.forEach(function (card) {
            var tags = card.getAttribute('data-tags').split(' ');

            if (selectedTags.length === 0) {
                card.style.display = 'block';
            } else {
                var isMatch = selectedTags.some(tag => tags.includes(tag));
                card.style.display = isMatch ? 'block' : 'none';
            }
        });
    }

    // Attach event listeners to all checkboxes
    document.querySelectorAll('.form-check-input').forEach(function (checkbox) {
        checkbox.addEventListener('change', filterNews);
    });

    // Mobile filter toggle
    const filterToggleButton = document.querySelector(".filter-toggle");
    const filterCard = document.querySelector(".filter-card");

    if (filterToggleButton && filterCard) {
        filterToggleButton.addEventListener("click", function () {
            filterCard.classList.toggle("active");

            // Optional: Smooth scroll to the filter when opened
            if (filterCard.classList.contains("active")) {
                filterCard.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        });
    }
    document.addEventListener("DOMContentLoaded", function () {
        const ticker = document.querySelector(".news-ticker ul");
        if (ticker) {
            const clone = ticker.cloneNode(true);
            ticker.parentElement.appendChild(clone);
        }
    });
});
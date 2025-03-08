document.addEventListener("DOMContentLoaded", () => {
    gsap.registerPlugin(ScrollTrigger);

    // Fade-in animation for sections as they appear
    gsap.utils.toArray(".section-block").forEach((block) => {
        gsap.fromTo(
            block,
            { opacity: 0, y: 50 },
            {
                opacity: 1,
                y: 0,
                duration: 1,
                scrollTrigger: {
                    trigger: block,
                    start: "top 85%",
                    toggleActions: "play none none reverse",
                },
            }
        );
    });

    // Parallax effect for the header
    gsap.to(".parallax-header", {
        backgroundPosition: "50% 100%",
        ease: "none",
        scrollTrigger: {
            trigger: ".parallax-header",
            start: "top top",
            end: "bottom top",
            scrub: true
        }
    });

    // Fade-in animation for team members
    gsap.utils.toArray(".team-member").forEach((member) => {
        gsap.fromTo(member, 
            { opacity: 0, y: 50 }, 
            { 
                opacity: 1, 
                y: 0, 
                duration: 1, 
                scrollTrigger: {
                    trigger: member,
                    start: "top 85%",
                    toggleActions: "play none none reverse",
                },
            }
        );
    });

    // ✅ Ensure Show More Button Works
    document.querySelectorAll(".show-more-btn").forEach(button => {
        button.addEventListener("click", () => {
            let description = button.nextElementSibling;
            let arrow = button.querySelector(".arrow-icon");

            // Toggle visibility of description
            if (description.classList.contains("d-none")) {
                description.classList.remove("d-none");
                description.style.maxHeight = description.scrollHeight + "px"; // Expand smoothly
                arrow.style.transform = "rotate(180deg)";
            } else {
                description.style.maxHeight = "0";
                description.classList.add("d-none"); // Collapse smoothly
                arrow.style.transform = "rotate(0deg)";
            }
        });
    });

    // ✅ Ensure Bootstrap 5 Carousel Works
    let teamCarousel = document.querySelector("#teamCarousel");
    if (teamCarousel) {
        let carousel = new bootstrap.Carousel(teamCarousel, {
            interval: 5000, // Auto-slide every 5 seconds
            wrap: true, // Infinite looping
            pause: "hover" // Pause on hover
        });
    }

    // ✅ Fix Hover Pause for Partner Slider (Ensures Smooth Scrolling)
    document.querySelectorAll(".partners-slider").forEach(slider => {
        slider.addEventListener("mouseenter", () => {
            slider.style.animationPlayState = "paused";
        });

        slider.addEventListener("mouseleave", () => {
            slider.style.animationPlayState = "running";
        });
    });
});
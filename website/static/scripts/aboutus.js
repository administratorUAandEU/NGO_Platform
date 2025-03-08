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

    // Expand/Collapse Member Description
    document.querySelectorAll(".show-more-btn").forEach((button) => {
        button.addEventListener("click", () => {
            let description = button.nextElementSibling;
            let arrow = button.querySelector(".arrow-icon");

            if (description.classList.contains("active")) {
                gsap.to(description, { height: 0, opacity: 0, duration: 0.3, ease: "power2.out" });
                description.classList.remove("active");
                arrow.style.transform = "rotate(0deg)";
            } else {
                gsap.to(description, { height: "auto", opacity: 1, duration: 0.5, ease: "power2.inOut" });
                description.classList.add("active");
                arrow.style.transform = "rotate(180deg)";
            }
        });
    });
    document.addEventListener("DOMContentLoaded", () => {
        document.querySelectorAll(".partners-slider").forEach(slider => {
            slider.addEventListener("mouseenter", () => {
                slider.style.animationPlayState = "paused";
            });
    
            slider.addEventListener("mouseleave", () => {
                slider.style.animationPlayState = "running";
            });
        });
    });

});
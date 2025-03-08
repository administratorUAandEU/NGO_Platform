document.addEventListener("DOMContentLoaded", () => {
    gsap.registerPlugin(ScrollTrigger);

    // Parallax effect on scroll
    gsap.to(".parallax", {
        backgroundPosition: "50% 100%",
        ease: "none",
        scrollTrigger: {
            trigger: ".parallax",
            start: "top top",
            end: "bottom top",
            scrub: true
        }
    });
});
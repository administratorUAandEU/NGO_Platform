gsap.registerPlugin(ScrollTrigger);

let getRatio = el => window.innerHeight / (window.innerHeight + el.offsetHeight);

gsap.utils.toArray(".news-image-container").forEach((section, i) => {
    let bg = section.querySelector(".news-bg");

    gsap.fromTo(bg, {
        backgroundPosition: "50% 0px"
    }, {
        backgroundPosition: "50% 50px",
        ease: "none",
        scrollTrigger: {
            trigger: section,
            start: "top top",
            end: "bottom top",
            scrub: true,
            invalidateOnRefresh: true
        }
    });
});
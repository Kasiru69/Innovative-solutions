(function () {
    "use strict";

    const navbar = document.querySelector(".navbar");
    const toggle = document.querySelector(".navbar__toggle");
    const navLinks = document.querySelector(".navbar__links");
    const links = document.querySelectorAll('.navbar__links a[href^="#"]');
    const sections = document.querySelectorAll("section[id]");

    /* Navbar scroll effect */
    function onScroll() {
        if (window.scrollY > 40) {
            navbar.classList.add("navbar--scrolled");
        } else {
            navbar.classList.remove("navbar--scrolled");
        }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    /* Mobile menu */
    if (toggle && navLinks) {
        toggle.addEventListener("click", function () {
            const isOpen = navLinks.classList.toggle("is-open");
            toggle.classList.toggle("is-open", isOpen);
            toggle.setAttribute("aria-expanded", String(isOpen));
        });

        links.forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("is-open");
                toggle.classList.remove("is-open");
                toggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    /* Active nav link on scroll */
    function setActiveLink() {
        const scrollPos = window.scrollY + 120;

        sections.forEach(function (section) {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute("id");

            if (scrollPos >= top && scrollPos < top + height) {
                links.forEach(function (link) {
                    link.classList.remove("is-active");
                    if (link.getAttribute("href") === "#" + id) {
                        link.classList.add("is-active");
                    }
                });
            }
        });
    }

    window.addEventListener("scroll", setActiveLink, { passive: true });
    setActiveLink();

    /* Scroll reveal */
    const revealElements = document.querySelectorAll(
        ".section__header, .card, .timeline__step, .why-card, .about__content, .contact"
    );

    revealElements.forEach(function (el) {
        el.classList.add("reveal");
    });

    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
        );

        revealElements.forEach(function (el) {
            observer.observe(el);
        });
    } else {
        revealElements.forEach(function (el) {
            el.classList.add("is-visible");
        });
    }

    /* Contact form — submit without reloading the page */
    const contactForm = document.getElementById("contact-form");
    const contactAlert = document.getElementById("contact-alert");
    const contactSubmit = document.getElementById("contact-submit");

    function showContactAlert(text, type) {
        if (!contactAlert) return;
        contactAlert.textContent = text;
        contactAlert.className = "contact-alert alert alert--" + type;
        contactAlert.hidden = false;
    }

    function clearFieldErrors() {
        contactForm.querySelectorAll("[data-error]").forEach(function (el) {
            el.textContent = "";
            el.hidden = true;
        });
    }

    if (contactForm) {
        contactForm.addEventListener("submit", async function (event) {
            event.preventDefault();
            clearFieldErrors();
            if (contactAlert) contactAlert.hidden = true;

            const csrfInput = contactForm.querySelector("[name=csrfmiddlewaretoken]");
            const defaultLabel = contactSubmit.textContent;
            contactSubmit.disabled = true;
            contactSubmit.textContent = "Sending…";

            try {
                const response = await fetch(contactForm.action, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": csrfInput.value,
                        Accept: "application/json",
                    },
                    body: new URLSearchParams(new FormData(contactForm)),
                });

                const data = await response.json();

                if (response.ok && data.ok) {
                    contactForm.reset();
                    showContactAlert(data.message, "success");
                    return;
                }

                if (data.errors) {
                    Object.keys(data.errors).forEach(function (field) {
                        const errorEl = contactForm.querySelector('[data-error="' + field + '"]');
                        if (errorEl && data.errors[field].length) {
                            errorEl.textContent = data.errors[field][0].message;
                            errorEl.hidden = false;
                        }
                    });
                    showContactAlert("Please fix the errors below.", "error");
                    return;
                }

                showContactAlert(
                    data.message || "Something went wrong. Please try again.",
                    "error"
                );
            } catch (err) {
                showContactAlert("Network error. Please try again.", "error");
            } finally {
                contactSubmit.disabled = false;
                contactSubmit.textContent = defaultLabel;
            }
        });
    }
})();

/* Store UX helpers (dark + purple theme) */
(function () {
    "use strict";

    /* ============ Mobile nav toggle ============ */
    const navToggle = document.querySelector(".nav-toggle");
    const navLinks = document.getElementById("primary-nav");
    if (navToggle && navLinks) {
        const closeMenu = () => {
            navLinks.classList.remove("is-open");
            navToggle.classList.remove("is-active");
            navToggle.setAttribute("aria-expanded", "false");
            document.body.classList.remove("nav-open");
        };
        navToggle.addEventListener("click", () => {
            const open = navLinks.classList.toggle("is-open");
            navToggle.classList.toggle("is-active", open);
            navToggle.setAttribute("aria-expanded", String(open));
            document.body.classList.toggle("nav-open", open);
        });
        navLinks.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeMenu));
        window.addEventListener("resize", () => { if (window.innerWidth > 640) closeMenu(); });
        document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeMenu(); });
    }

    /* ============ Image fade-in once loaded ============
       Solves the "thumbnail is huge while loading" feel.
       The CSS sets opacity:0 by default; this flips to 1 when the image is decoded. */
    document.querySelectorAll("img.product-image, .product-detail-image img, .cart-thumb img").forEach((img) => {
        if (img.complete && img.naturalWidth > 0) {
            img.classList.add("is-loaded");
        } else {
            img.addEventListener("load",  () => img.classList.add("is-loaded"), { once: true });
            img.addEventListener("error", () => img.classList.add("is-loaded"), { once: true }); // fail-open so the card isn't blank
        }
    });

    /* ============ Add-to-cart button feedback ============
       Briefly changes the label to "Added!" before letting the form submit. */
    document.querySelectorAll("form[action^='/cart/add/'] button[type='submit']").forEach((btn) => {
        btn.addEventListener("click", () => {
            if (btn.dataset.busy === "1") return;
            btn.dataset.busy = "1";
            const original = btn.textContent;
            btn.textContent = "Added!";
            btn.style.filter = "brightness(1.2)";
            setTimeout(() => {
                btn.textContent = original;
                btn.style.filter = "";
                btn.dataset.busy = "0";
            }, 900);
        }, { capture: true });
    });

    /* ============ Flash messages auto-dismiss ============ */
    document.querySelectorAll(".flash").forEach((f) => {
        setTimeout(() => {
            f.style.transition = "opacity .4s, transform .4s";
            f.style.opacity = "0";
            f.style.transform = "translateY(-8px)";
            setTimeout(() => f.remove(), 400);
        }, 5000);
    });

    /* ============ Scroll-to-top button ============ */
    const scrollTopBtn = document.querySelector(".scroll-top");
    if (scrollTopBtn) {
        const onScroll = () => {
            if (window.scrollY > 400) scrollTopBtn.classList.add("is-visible");
            else scrollTopBtn.classList.remove("is-visible");
        };
        window.addEventListener("scroll", onScroll, { passive: true });
        scrollTopBtn.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
})();

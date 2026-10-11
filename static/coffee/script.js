const menuToggle = document.querySelector(".menu-toggle");
const primaryNav = document.querySelector(".primary-nav");
const pageLoader = document.querySelector("#page-loader");

if (pageLoader) {
  const startedAt = performance.now();
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const minimumDisplay = reduceMotion.matches ? 0 : 560;
  let hideScheduled = false;
  let loaderFailsafe = 0;

  function hidePageLoader() {
    if (hideScheduled) return;
    hideScheduled = true;
    window.clearTimeout(loaderFailsafe);

    const remaining = Math.max(0, minimumDisplay - (performance.now() - startedAt));
    window.setTimeout(() => {
      document.documentElement.classList.add("page-ready");
      pageLoader.classList.add("is-leaving");
      pageLoader.setAttribute("aria-hidden", "true");
      pageLoader.inert = true;

      window.setTimeout(() => pageLoader.remove(), reduceMotion.matches ? 0 : 380);
    }, remaining);
  }

  loaderFailsafe = window.setTimeout(hidePageLoader, 8000);
  if (document.readyState === "complete") {
    hidePageLoader();
  } else {
    window.addEventListener("load", hidePageLoader, { once: true });
  }

  window.addEventListener("pageshow", (event) => {
    if (event.persisted) {
      window.clearTimeout(loaderFailsafe);
      document.documentElement.classList.add("page-ready");
      pageLoader.remove();
    }
  });
}

function setMenuOpen(isOpen) {
  menuToggle.setAttribute("aria-expanded", String(isOpen));
  menuToggle.setAttribute("aria-label", isOpen ? "Close navigation menu" : "Open navigation menu");
  primaryNav.classList.toggle("is-open", isOpen);
}

menuToggle.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  setMenuOpen(!isOpen);
});

primaryNav.addEventListener("click", (event) => {
  if (event.target.closest("a")) setMenuOpen(false);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuToggle.getAttribute("aria-expanded") === "true") {
    setMenuOpen(false);
    menuToggle.focus();
  }
});

document.addEventListener("click", (event) => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  if (isOpen && !primaryNav.contains(event.target) && !menuToggle.contains(event.target)) {
    setMenuOpen(false);
  }
});

const revealElements = [...document.querySelectorAll("[data-scroll-reveal]")];
const reduceMotionPreference = window.matchMedia("(prefers-reduced-motion: reduce)");

if (revealElements.length && "IntersectionObserver" in window && !reduceMotionPreference.matches) {
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("has-entered");
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: "0px 0px -5% 0px",
  });

  const siblingIndexes = new Map();
  revealElements.forEach((element) => {
    const parent = element.parentElement;
    const index = siblingIndexes.get(parent) || 0;
    siblingIndexes.set(parent, index + 1);
    element.style.setProperty("--scroll-delay", `${Math.min(index, 3) * 70}ms`);
    revealObserver.observe(element);
  });

  document.documentElement.classList.add("scroll-motion-ready");
}

document.querySelector("#current-year").textContent = new Date().getFullYear();

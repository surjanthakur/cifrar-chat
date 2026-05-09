const mobileBtn = document.getElementById("mobile-menu-button");
const mobileMenu = document.getElementById("mobile-menu");

if (mobileBtn && mobileMenu) {
  mobileBtn.addEventListener("click", () => {
    mobileMenu.classList.toggle("hidden");

    const icon = mobileBtn.querySelector("i");
    if (!icon) {
      return;
    }

    if (icon.classList.contains("fa-bars")) {
      icon.classList.remove("fa-bars");
      icon.classList.add("fa-xmark");
    } else {
      icon.classList.remove("fa-xmark");
      icon.classList.add("fa-bars");
    }
  });

  document.querySelectorAll("#mobile-menu a").forEach((link) => {
    link.addEventListener("click", () => {
      mobileMenu.classList.add("hidden");
    });
  });
}

const themeToggle = document.getElementById("theme-toggle");
const html = document.documentElement;

if (themeToggle) {
  if (
    localStorage.theme === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    html.classList.add("dark");
  }

  themeToggle.addEventListener("click", () => {
    if (html.classList.contains("dark")) {
      html.classList.remove("dark");
      localStorage.theme = "light";
      themeToggle.innerHTML = `<i class="fa-solid fa-moon text-lg"></i>`;
    } else {
      html.classList.add("dark");
      localStorage.theme = "dark";
      themeToggle.innerHTML = `<i class="fa-solid fa-sun text-lg"></i>`;
    }
  });
}

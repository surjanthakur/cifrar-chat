const mobileBtn = document.getElementById("mobile-menu-button");
const mobileMenu = document.getElementById("mobile-menu");

mobileBtn.addEventListener("click", () => {
  mobileMenu.classList.toggle("hidden");

  // Optional: Change icon between bars and x
  const icon = mobileBtn.querySelector("i");
  if (icon.classList.contains("fa-bars")) {
    icon.classList.remove("fa-bars");
    icon.classList.add("fa-xmark");
  } else {
    icon.classList.remove("fa-xmark");
    icon.classList.add("fa-bars");
  }
});

// Optional: Close mobile menu when clicking a link
document.querySelectorAll("#mobile-menu a").forEach((link) => {
  link.addEventListener("click", () => {
    mobileMenu.classList.add("hidden");
  });
});

// Simple Dark Mode Toggle
const themeToggle = document.getElementById("theme-toggle");
const html = document.documentElement;

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

(function () {
  var root = document.documentElement;
  var button = document.getElementById("theme-toggle");
  if (!button) return;

  function current() {
    return root.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function setTheme(theme) {
    root.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("borelo-theme", theme);
    } catch (e) {}
    button.setAttribute("aria-pressed", theme === "dark" ? "true" : "false");
  }

  button.addEventListener("click", function () {
    setTheme(current() === "dark" ? "light" : "dark");
  });

  button.setAttribute("aria-pressed", current() === "dark" ? "true" : "false");
})();

const toggle = document.getElementById("themeSwitch");
const root = document.documentElement;
const modeLabel = document.getElementById("modeLabel");

toggle.addEventListener("change", () => {
  if (toggle.checked) {
    root.classList.remove("dark");
    root.classList.add("light");
    modeLabel.textContent = "☼";
  } else {
    root.classList.remove("light");
    root.classList.add("dark");
    modeLabel.textContent = "☽";
  }
});

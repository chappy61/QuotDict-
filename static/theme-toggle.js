const toggle = document.getElementById("themeSwitch");
const root = document.documentElement;
const modeLabel = document.getElementById("modeLabel");
const themeStyleLink = document.getElementById("theme-style");  // <link id="theme-style">をheadに用意しておく

toggle.addEventListener("change", () => {
  if (toggle.checked) {
    root.classList.remove("dark");
    root.classList.add("light");
    modeLabel.textContent = "☼";

    // highlight.js のテーマ切り替え（ライトモード用の自作CSSに）
    themeStyleLink.href = "/static/style.css";  // 自作のライトテーマCSSファイルを用意する
  } else {
    root.classList.remove("light");
    root.classList.add("dark");
    modeLabel.textContent = "☽";

    // highlight.js のテーマ切り替え（ダークモード用CDN）
    themeStyleLink.href = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github-dark.min.css";
  }
});

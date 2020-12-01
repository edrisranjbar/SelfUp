document.querySelector(".menu_icon").addEventListener("click", () => {
    let elem = document.querySelector(".menu ul");
    let body = document.querySelector("body");
    if (elem.style.display === "block") {
        elem.style.display = "none"
        body.style.height = "unset";
        body.style.overflow = "unset";
    } else {
        elem.style.display = "block"
        body.style.height = "100vh";
        body.style.overflow = "hidden";
    }
})
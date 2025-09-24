document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("menu-toggle");
    const dropdown = document.getElementById("menu-dropdown");
    const ellipsisToggle = document.getElementById("ellipsis-toggle");
    const ellipsisDropdown = document.getElementById("ellipsis-dropdown");

    // Menu hambúrguer
    toggle?.addEventListener("click", () => {
        dropdown.style.display =
            dropdown.style.display === "flex" ? "none" : "flex";
    });

    // Menu 3 pontos
    ellipsisToggle?.addEventListener("click", () => {
        ellipsisDropdown.style.display =
            ellipsisDropdown.style.display === "flex" ? "none" : "flex";
    });

    // Fecha dropdowns ao clicar fora
    document.addEventListener("click", (e) => {
        if (!toggle?.contains(e.target) && !dropdown?.contains(e.target)) {
            if (dropdown) dropdown.style.display = "none";
        }
        if (!ellipsisToggle?.contains(e.target) && !ellipsisDropdown?.contains(e.target)) {
            if (ellipsisDropdown) ellipsisDropdown.style.display = "none";
        }
    });
});

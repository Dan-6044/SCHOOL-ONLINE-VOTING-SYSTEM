document.addEventListener("DOMContentLoaded", function () {
    function showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll(".content-section").forEach(section => {
            section.classList.add("d-none");
        });

        // Remove active class from all sidebar links
        document.querySelectorAll(".nav-link").forEach(link => {
            link.classList.remove("active-section");
        });

        // Show the selected section
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.remove("d-none");
        }

        // Highlight the active link
        const activeLink = document.querySelector(`.nav-link[onclick="showSection('${sectionId}')"]`);
        if (activeLink) {
            activeLink.classList.add("active-section");
        }

        // Save the selected section in local storage
        localStorage.setItem("activeSection", sectionId);
    }

    // Load the last active section or default to dashboard
    const lastSection = localStorage.getItem("activeSection") || "dashboard";
    showSection(lastSection);
});

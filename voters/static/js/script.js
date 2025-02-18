document.addEventListener("DOMContentLoaded", function () {
    const sectionLinks = document.querySelectorAll(".section-link");
    const contentBox = document.getElementById("contentBox");
    const defaultContent = document.getElementById("defaultContent");
    const dynamicContent = document.getElementById("dynamicContent");

    sectionLinks.forEach(link => {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            const sectionId = this.getAttribute("data-section");

            // Hide the default content
            defaultContent.classList.add("d-none");

            // Show dynamic content
            dynamicContent.classList.remove("d-none");

            // Fetch content from the Django template
            fetch(`/${sectionId}/`)  // Ensure you have URL patterns in Django
                .then(response => response.text())
                .then(html => {
                    dynamicContent.innerHTML = html;
                })
                .catch(error => {
                    console.error("Error loading content:", error);
                    dynamicContent.innerHTML = "<p>Failed to load content.</p>";
                });
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const backToTopBtn = document.getElementById("backToTopBtn");

    window.addEventListener("scroll", function () {
        if (window.scrollY > 250) {
            backToTopBtn?.classList.add("show");
        } else {
            backToTopBtn?.classList.remove("show");
        }
    });

    backToTopBtn?.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    const alerts = document.querySelectorAll(".alert");
    alerts.forEach((alertBox) => {
        setTimeout(() => {
            if (alertBox.classList.contains("show")) {
                alertBox.classList.remove("show");
            }
        }, 4500);
    });

    const profileImageInput = document.getElementById("id_image");
    const profileImagePreview = document.getElementById("profileImagePreview");

    if (profileImageInput && profileImagePreview) {
        profileImageInput.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function (e) {
                profileImagePreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        });
    }

    const dashboardSearch = document.getElementById("dashboardSearch");
    const dashboardCards = document.querySelectorAll("[data-search-card]");
    const dashboardCount = document.getElementById("resultCount");

    if (dashboardSearch && dashboardCards.length) {
        const updateCount = () => {
            const visibleCards = [...dashboardCards].filter(card => card.style.display !== "none").length;
            if (dashboardCount) {
                dashboardCount.textContent = `${visibleCards} result${visibleCards === 1 ? "" : "s"} found`;
            }
        };

        dashboardSearch.addEventListener("input", function () {
            const term = this.value.trim().toLowerCase();

            dashboardCards.forEach((card) => {
                const haystack = card.dataset.searchText.toLowerCase();
                card.style.display = haystack.includes(term) ? "" : "none";
            });

            updateCount();
        });

        updateCount();
    }

    const feedbackTextarea = document.getElementById("id_comment");
    const feedbackCounter = document.getElementById("feedbackCounter");

    if (feedbackTextarea && feedbackCounter) {
        const syncCounter = () => {
            feedbackCounter.textContent = `${feedbackTextarea.value.length} characters`;
        };

        feedbackTextarea.addEventListener("input", syncCounter);
        syncCounter();
    }

    const courseSearch = document.getElementById("courseSearch");
    const courseCards = document.querySelectorAll("[data-course-card]");
    const courseEmptyState = document.getElementById("courseEmptyState");

    if (courseSearch && courseCards.length) {
        courseSearch.addEventListener("input", function () {
            const term = this.value.trim().toLowerCase();
            let visible = 0;

            courseCards.forEach((card) => {
                const text = card.dataset.courseText.toLowerCase();
                const match = text.includes(term);
                card.style.display = match ? "" : "none";
                if (match) visible += 1;
            });

            if (courseEmptyState) {
                courseEmptyState.style.display = visible === 0 ? "block" : "none";
            }
        });
    }
});
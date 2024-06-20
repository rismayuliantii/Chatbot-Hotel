const testimonialItems = document.querySelectorAll(".testimonial-item");
const prevBtn = document.querySelector(".prev-btn");
const nextBtn = document.querySelector(".next-btn");

let currentIndex = 0;

function showTestimonial(index) {
    testimonialItems.forEach((item, i) => {
        if (i === index) {
            item.style.display = "block";
        } else {
            item.style.display = "none";
        }
    });
}

prevBtn.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + testimonialItems.length) % testimonialItems.length;
    showTestimonial(currentIndex);
});

nextBtn.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % testimonialItems.length;
    showTestimonial(currentIndex);
});

// Tampilkan testimoni pertama saat halaman dimuat
showTestimonial(currentIndex);


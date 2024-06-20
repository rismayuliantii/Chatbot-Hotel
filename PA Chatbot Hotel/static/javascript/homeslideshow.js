  document.addEventListener('DOMContentLoaded', function() {
    const heroSlider = document.querySelector('.hero-slider');
    const slides = heroSlider.querySelectorAll('.slide');
    let currentSlide = 0;

    function showSlide(index) {
      slides.forEach(slide => {
        slide.classList.remove('active');
        slide.classList.remove('next');
      });
      slides[index].classList.add('active');
      slides[(index + 1) % slides.length].classList.add('next');
      currentSlide = index;
    }

    function nextSlide() {
      let nextIndex = (currentSlide + 1) % slides.length;
      showSlide(nextIndex);
    }

    setInterval(nextSlide, 7000); // Interval 7 detik
    showSlide(0); // Tampilkan slide pertama
  });
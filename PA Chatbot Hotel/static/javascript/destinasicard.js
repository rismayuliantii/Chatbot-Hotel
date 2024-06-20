const prevBtn = document.querySelector('.prev-btna');
const nextBtn = document.querySelector('.next-btna');
const destinationCards = document.querySelector('.destination-cards');
let currentIndex = 0;
const cardWidth = 340; // Lebar setiap kartu ditambah margin kiri dan kanan
const containerWidth = document.querySelector('.destination-cards-container').offsetWidth - 40; // Mengurangi lebar container dengan total padding kiri dan kanan
let maxIndex = Math.max(0, Math.ceil(destinationCards.children.length / 3) - Math.floor(containerWidth / cardWidth / 3));

function updateMaxIndex() {
  maxIndex = Math.max(0, Math.ceil(destinationCards.children.length / 3) - Math.floor(containerWidth / cardWidth / 3));
}

prevBtn.addEventListener('click', () => {
  if (currentIndex > 0) {
    currentIndex--;
  } else {
    currentIndex = maxIndex;
  }
  destinationCards.style.transform = `translateX(-${currentIndex * cardWidth * 3}px)`;
});

nextBtn.addEventListener('click', () => {
  if (currentIndex < maxIndex) {
    currentIndex++;
  } else {
    currentIndex = 0;
  }
  destinationCards.style.transform = `translateX(-${currentIndex * cardWidth * 3}px)`;
});

// Panggil updateMaxIndex setiap kali ada perubahan pada kartu destinasi
const observer = new MutationObserver(updateMaxIndex);
observer.observe(destinationCards, { childList: true });

// Panggil updateMaxIndex saat halaman dimuat untuk memeriksa jumlah kartu awal
updateMaxIndex();
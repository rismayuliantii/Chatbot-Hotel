const searchBtn = document.querySelector('.serc-btn');
const closeBtn = document.querySelector('.closea-btn');
const headerContainer = document.querySelector('.header-container');
const imageContainer = document.querySelector('.image-container');
const formContainer = document.querySelector('.form-container');

searchBtn.addEventListener('click', function() {
  headerContainer.classList.add('slide-left');
  imageContainer.classList.add('slide-left');
  formContainer.classList.add('show');
});

closeBtn.addEventListener('click', function() {
  headerContainer.classList.remove('slide-left');
  imageContainer.classList.remove('slide-left');
  formContainer.classList.remove('show');
});
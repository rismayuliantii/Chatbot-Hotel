function toggleProfileMenu() {
  var profileMenu = document.getElementById("profile-menu");
  profileMenu.style.display = profileMenu.style.display === "block" ? "none" : "block";
}

document.addEventListener("click", function(event) {
  var profileMenu = document.getElementById("profile-menu");
  var loginBtn = document.querySelector(".login");
  if (!loginBtn.contains(event.target)) {
    profileMenu.style.display = "none";
  }
});

window.addEventListener("scroll", function() {
  var chatbotBtn = document.getElementById("chatbot-btn");
  var chatbotCapsule = document.getElementById("chatbot-capsule");
  var navbarHeight = document.querySelector("nav").offsetHeight;

  if (window.pageYOffset > navbarHeight) {
    chatbotBtn.style.display = "none";
    chatbotCapsule.style.display = "flex";
    chatbotCapsule.style.transition = "all 0.3s ease"; // Tambahkan transisi saat chatbot-capsule muncul
  } else {
    chatbotBtn.style.display = "inline-block";
    chatbotCapsule.style.display = "none";
    chatbotCapsule.style.transition = "all 0.3s ease"; // Tambahkan transisi saat chatbot-capsule hilang
  }
});
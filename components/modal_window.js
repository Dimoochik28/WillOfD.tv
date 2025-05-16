// ==== МОДАЛЬНЕ ВІКНО ====
const modal = document.getElementById("modal");
const closeButton = document.querySelector(".close-button");

// Відкриття модального вікна
document.querySelectorAll(".button-login").forEach((button) => {
  button.addEventListener("click", () => {
    modal.style.display = "block";
  });
});

// Закриття по кнопці "X"
closeButton.addEventListener("click", () => {
  modal.style.display = "none";
});

// Закриття при кліку поза формою
window.addEventListener("click", (event) => {
  if (event.target === modal) {
    modal.style.display = "none";
  }
});

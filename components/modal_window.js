const modal = document.getElementById("modal");
const closeButton = modal.querySelector(".close-button");
const modalTitle = document.getElementById("modal-title");

document.querySelectorAll(".button-login").forEach((button) => {
  button.addEventListener("click", (e) => {
    const action = button.getAttribute("data-action");

    // Показати заголовок залежно від кнопки
    if (action === "register") {
      modalTitle.textContent = "Реєстрація";
    } else if (action === "login") {
      modalTitle.textContent = "Вхід";
    }

    // Відкрити модальне вікно
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

// Отримуємо модальні вікна
const modalRegister = document.getElementById("modal-register");
const modalLogin = document.getElementById("modal-login");

// Кнопки відкриття
const openRegisterBtn = document.querySelector(".button-register");
const openLoginBtn = document.querySelector(".button-login");

// Закриття всіх модальних вікон
const closeButtons = document.querySelectorAll(".close-button");

// Відкрити модальне для реєстрації
openRegisterBtn.addEventListener("click", () => {
  modalRegister.style.display = "block";
});

// Відкрити модальне для входу
openLoginBtn.addEventListener("click", () => {
  modalLogin.style.display = "block";
});

// Закриття по хрестику
closeButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    modalRegister.style.display = "none";
    modalLogin.style.display = "none";
  });
});

// Закриття при кліку поза формою
window.addEventListener("click", (event) => {
  if (event.target === modalRegister) {
    modalRegister.style.display = "none";
  }
  if (event.target === modalLogin) {
    modalLogin.style.display = "none";
  }
});

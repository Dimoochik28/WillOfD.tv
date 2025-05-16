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

// ==== ОБРОБКА РЕЄСТРАЦІЇ ====
document
  .getElementById("registration-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const username = formData.get("username");
    const email = formData.get("email");
    const password = formData.get("password");

    try {
      const response = await fetch("/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });

      const result = await response.json();

      if (response.ok) {
        alert("Реєстрація успішна!");
        modal.style.display = "none";
        this.reset(); // Очистити форму
      } else {
        alert("Помилка: " + result.message);
      }
    } catch (error) {
      alert("Помилка підключення до сервера");
      console.error(error);
    }
  });

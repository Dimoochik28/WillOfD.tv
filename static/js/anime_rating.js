const stars = document.querySelectorAll(".star");
const ratingValue = document.getElementById("rating-value");
const rateButton = document.querySelector(".rating-button");
const ratingContainer = document.querySelector(".rating");
const animeId = ratingContainer.dataset.animeId;
const savedRating = parseInt(ratingContainer.dataset.userRating || 0);

let currentRating = savedRating;

function updateStars(rating) {
  stars.forEach((s) => s.classList.remove("selected"));
  for (let i = 0; i < rating; i++) {
    stars[i].classList.add("selected");
  }
}

// Автозаповнення збереженого рейтингу
if (savedRating > 0) {
  updateStars(savedRating);
}

stars.forEach((star, index) => {
  star.addEventListener("click", () => {
    currentRating = parseInt(star.dataset.value);
    ratingValue.textContent = `Оцінка: ${currentRating}`;
    updateStars(currentRating);
  });

  star.addEventListener("mouseover", () => {
    stars.forEach((s) => s.classList.remove("hovered"));
    for (let i = 0; i <= index; i++) {
      stars[i].classList.add("hovered");
    }
  });

  star.addEventListener("mouseout", () => {
    stars.forEach((s) => s.classList.remove("hovered"));
  });
});

if (rateButton) {
  rateButton.addEventListener("click", () => {
    if (currentRating === 0) {
      alert("Будь ласка, виберіть оцінку.");
      return;
    }

    fetch("/rate_anime", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        anime_id: animeId,
        rating: currentRating,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message || "Оцінка надіслана!");
        // Оновлення тексту після оцінки
        ratingValue.textContent = `Оцінка: ${currentRating}`;
        document.getElementById(
          "rating-title"
        ).textContent = `Ви оцінили на ${currentRating} / 5`;
        rateButton.remove(); // Приховати кнопку
      })
      .catch((error) => {
        alert("Помилка при відправці оцінки.");
        console.error(error);
      });
  });
}

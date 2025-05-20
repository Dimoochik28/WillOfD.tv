document.addEventListener("DOMContentLoaded", () => {
  const animeList = document.getElementById("anime-list");

  for (const key in window.animeData) {
    const anime = window.animeData[key];

    const card = document.createElement("div");
    card.classList.add("card");

    const link = document.createElement("a");
    link.href = `anime_episodes.html?key=${key}`;

    const img = document.createElement("img");
    img.classList.add("logo-of-anime");
    img.src = anime.cover;
    img.alt = anime.title;

    const h3 = document.createElement("h3");
    h3.textContent = anime.title;

    link.appendChild(img);
    link.appendChild(h3);
    card.appendChild(link);
    animeList.appendChild(card);
  }
});

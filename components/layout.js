document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const key = params.get("key");

  const anime = window.animeData[key];
  if (!anime) {
    document.getElementById("anime-title").textContent = "Anime not found";
    return;
  }

  const titleEl = document.getElementById("anime-title");
  const descEl = document.getElementById("anime-description");
  const container = document.getElementById("episode-list");
  const template = document.getElementById("episode-template");

  titleEl.textContent = anime.title;
  descEl.textContent = anime.description;
  container.innerHTML = "";

  let seasonCounter = 1;

  anime.seasons.forEach((season, seasonIndex) => {
    // Додаємо заголовок сезону
    const seasonHeader = document.createElement("h2");
    seasonHeader.textContent = season.seasonTitle || `Сезон ${seasonCounter++}`;
    container.appendChild(seasonHeader);

    // Додаємо епізоди
    for (let i = 1; i <= season.episodes; i++) {
      const clone = template.content.cloneNode(true);
      clone.querySelector(".episode-number").textContent = i;
      clone.querySelector("button").addEventListener("click", () => {
        window.location.href = `episode.html?key=${key}&season=${
          seasonIndex + 1
        }&episode=${i}`;
      });
      container.appendChild(clone);
    }
  });
});

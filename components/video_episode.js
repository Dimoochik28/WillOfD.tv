document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const key = params.get("key");
  const episode = parseInt(params.get("episode") || "1");

  // === Відео за аніме ===
  const animeVideos = {
    onepiece: { 1: "Video/onepiece/onepiece_trailer.mp4" },
    naruto: { 1: "Video/naruto/naruto_trailer.mp4" },
    boruto: { 1: "Video/boruto/boruto_trailer.mp4" },
    bleach: { 1: "Video/dleach/bleach_trailer.mp4" },
    drstone: { 1: "Video/drstone/drStone_trailer.mp4" },
    blackclover: { 1: "Video/blackclover/blackclover_trailer.mp4" },
    vanitasnokarte: { 1: "Video/vanitasnokarte/vanitasnokarte_trailer.mp4" },
    sololeveling: { 1: "Video/sololeveling/sololeveling_trailer.mp4" },
  };

  const video = document.getElementById("anime-video");
  const source = document.getElementById("video-source");

  if (animeVideos[key] && animeVideos[key][episode]) {
    source.src = animeVideos[key][episode];
    video.load();
  } else if (animeVideos[key]) {
    const firstAvailable = Object.values(animeVideos[key])[0];
    source.src = firstAvailable;
    video.load();
  } else {
    source.src = "";
    video.outerHTML = "<p>Відео не знайдено для цього епізоду.</p>";
  }

  // === Дані аніме ===
  const anime = window.animeData[key];
  let totalEpisodes = 1;

  if (anime && anime.seasons.length > 0) {
    totalEpisodes = anime.seasons.reduce(
      (sum, season) => sum + season.episodes,
      0
    );
  }

  // === Оновлення заголовку серії ===
  if (anime) {
    document.getElementById("title").textContent = anime.title;
    document.getElementById("anime-title").textContent = anime.title;
    document.getElementById("episode-number").textContent = `Серія ${episode}`;
    const coverImg = document.getElementById("anime-cover");
    coverImg.src = anime.cover;
    coverImg.alt = `${anime.title} Cover`;
    document.getElementById(
      "anime-cover-link"
    ).href = `anime_episods.html?key=${key}`;
  }

  // === Обробка кнопок ===
  const prevBtn = document.getElementById("prev-episode");
  const nextBtn = document.getElementById("next-episode");
  const allBtn = document.getElementById("all-episodes");

  if (episode > 1) {
    prevBtn.addEventListener("click", () => {
      window.location.href = `episode.html?key=${key}&episode=${episode - 1}`;
    });
  } else {
    prevBtn.style.display = "none";
  }

  if (episode < totalEpisodes) {
    nextBtn.addEventListener("click", () => {
      window.location.href = `episode.html?key=${key}&episode=${episode + 1}`;
    });
  } else {
    nextBtn.style.display = "none";
  }

  allBtn.addEventListener("click", () => {
    window.location.href = `anime_episods.html?key=${key}`;
  });
});

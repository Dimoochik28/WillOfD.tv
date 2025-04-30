document.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const key = params.get("key");
  const episode = params.get("episode");

  const animeVideos = {
    onepiece: {
      1: "Video/onepiece_trailer.mp4",
    },
    naruto: {
      1: "Video/naruto_trailer.mp4",
    },
    boruto: {
      1: "Video/boruto_trailer.mp4",
    },
    bleach: {
      1: "Video/bleach_trailer.mp4",
    },
    drstone: {
      1: "Video/drStone_trailer.mp4",
    },
    blackclover: {
      1: "Video/blackclover_trailer.mp4",
    },
    vanitasnokarte: {
      1: "Video/vanitasnokarte_trailer.mp4",
    },
    sololeveling: {
      1: "Video/sololeveling_trailer.mp4",
    },
  };

  const video = document.getElementById("anime-video");
  const source = document.getElementById("video-source");

  if (animeVideos[key] && animeVideos[key][episode]) {
    //якщо є завантажені серії видає їх
    source.src = animeVideos[key][episode];
    video.load();
  } else if (animeVideos[key]) {
    // Якщо більш серій немає, беремо трейлер
    const firstAvailable = Object.values(animeVideos[key])[0];
    source.src = firstAvailable;
    video.load();
  } else {
    // fallback — якщо нема відео
    source.src = "";
    video.outerHTML = "<p>Відео не знайдено для цього епізоду.</p>";
  }
});

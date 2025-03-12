document.getElementById("searchBtn").addEventListener("click", function () {
  let query = document.getElementById("searchInput").value.toLowerCase();
  alert("Пошук за запитом: " + query);
});

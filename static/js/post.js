(function () {
  "use strict";

  var article = document.querySelector("article.post[data-slug]");
  if (!article) return;

  var slug = article.dataset.slug;
  var viewEl = document.getElementById("view-count");
  var likeEl = document.getElementById("like-count");
  var button = document.getElementById("like-button");
  var likedKey = "borelo-liked:" + slug;

  function updateCounts(data) {
    if (!data) return;
    if (viewEl && typeof data.views === "number") viewEl.textContent = data.views;
    if (likeEl && typeof data.likes === "number") likeEl.textContent = data.likes;
  }

  function post(path) {
    return fetch(path, {
      method: "POST",
      headers: { Accept: "application/json" }
    }).then(function (res) {
      if (!res.ok) throw new Error("request failed");
      return res.json();
    });
  }

  function markLiked() {
    if (!button) return;
    button.classList.add("is-liked");
    button.disabled = true;
    button.textContent = "已赞";
  }

  post("/api/view/" + encodeURIComponent(slug))
    .then(updateCounts)
    .catch(function () {});

  var alreadyLiked = false;
  try {
    alreadyLiked = localStorage.getItem(likedKey) === "1";
  } catch (e) {}

  if (alreadyLiked) markLiked();

  if (button) {
    button.addEventListener("click", function () {
      if (button.disabled) return;
      button.disabled = true;
      post("/api/like/" + encodeURIComponent(slug))
        .then(function (data) {
          updateCounts(data);
          try {
            localStorage.setItem(likedKey, "1");
          } catch (e) {}
          markLiked();
        })
        .catch(function () {
          button.disabled = false;
        });
    });
  }
})();

(function () {
  var article = document.querySelector("article.post[data-slug]");
  if (!article) return;

  var slug = article.getAttribute("data-slug");
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
      headers: { Accept: "application/json" },
    }).then(function (res) {
      if (!res.ok) throw new Error("request failed");
      return res.json();
    });
  }

  post("/api/view/" + encodeURIComponent(slug))
    .then(updateCounts)
    .catch(function () {});

  var alreadyLiked = false;
  try {
    alreadyLiked = localStorage.getItem(likedKey) === "1";
  } catch (e) {}

  if (alreadyLiked && button) {
    button.classList.add("is-liked");
    button.disabled = true;
    button.textContent = "已赞";
  }

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
          button.classList.add("is-liked");
          button.textContent = "已赞";
        })
        .catch(function () {
          button.disabled = false;
        });
    });
  }
})();

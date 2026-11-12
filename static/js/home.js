(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ─────────────────────── cover: pointer parallax ───────────────────────
     The idle drift is a CSS animation on `transform`; this script only adds
     a `translate` offset on top of it. Individual transform properties
     compose, so the two never fight, and the browser interpolates the
     pointer response via `transition` — no requestAnimationFrame loop and
     nothing running on the main thread while the pointer is still. */

  var cover = document.querySelector(".cover");
  var finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  if (cover && finePointer && !reduceMotion) {
    var layers = [];

    function track(selector, depth) {
      var el = cover.querySelector(selector);
      if (el) layers.push({ el: el, depth: depth });
    }

    track(".figure-left", -1.15);
    track(".figure-mid", 0.6);
    track(".figure-right", 1.15);
    track(".reflect", 0.4);

    if (layers.length) {
      cover.addEventListener(
        "pointermove",
        function (event) {
          var rect = cover.getBoundingClientRect();
          var nx = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
          var ny = ((event.clientY - rect.top) / rect.height - 0.5) * 2;

          for (var i = 0; i < layers.length; i++) {
            var layer = layers[i];
            var x = nx * 26 * layer.depth;
            var y = ny * 15 * layer.depth;
            layer.el.style.translate =
              x.toFixed(2) + "px " + y.toFixed(2) + "px";
          }
        },
        { passive: true }
      );

      cover.addEventListener(
        "pointerleave",
        function () {
          for (var i = 0; i < layers.length; i++) {
            layers[i].el.style.translate = "0px 0px";
          }
        },
        { passive: true }
      );
    }
  }

  /* ─────────────────────── entries: float on every pass ───────────────────────
     Unlike a once-only reveal, entries re-arm when they leave the viewport,
     so scrolling back up replays the movement. Two separate thresholds act
     as hysteresis: an entry only re-arms once it is fully clear of the
     viewport, which keeps a row sitting on the boundary from flickering. */

  var entries = document.querySelectorAll(".entry");

  if (!entries.length) return;

  if (reduceMotion || !("IntersectionObserver" in window)) {
    for (var i = 0; i < entries.length; i++) {
      entries[i].classList.add("is-visible");
    }
    return;
  }

  var observer = new IntersectionObserver(
    function (records) {
      records.forEach(function (record) {
        if (record.isIntersecting) {
          record.target.classList.add("is-visible");
        } else {
          record.target.classList.remove("is-visible");
        }
      });
    },
    // Shrink the root so a row must be meaningfully on screen before it
    // floats in, and must leave entirely before it re-arms.
    { threshold: 0, rootMargin: "-8% 0px -12% 0px" }
  );

  for (var j = 0; j < entries.length; j++) {
    entries[j].style.transitionDelay = Math.min(j * 80, 320) + "ms";
    observer.observe(entries[j]);
  }
})();

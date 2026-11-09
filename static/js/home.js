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

    track(".figure-left", -1);
    track(".figure-mid", 0.5);
    track(".figure-right", 1);
    track(".reflect", 0.3);

    if (layers.length) {
      cover.addEventListener(
        "pointermove",
        function (event) {
          var rect = cover.getBoundingClientRect();
          var nx = ((event.clientX - rect.left) / rect.width - 0.5) * 2;
          var ny = ((event.clientY - rect.top) / rect.height - 0.5) * 2;

          for (var i = 0; i < layers.length; i++) {
            var layer = layers[i];
            var x = nx * 13 * layer.depth;
            var y = ny * 8 * layer.depth;
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

  /* ─────────────────────── entries: reveal on scroll ─────────────────────── */

  var entries = document.querySelectorAll(".entry");

  if (!entries.length) return;

  if (reduceMotion || !("IntersectionObserver" in window)) {
    for (var i = 0; i < entries.length; i++) {
      entries[i].classList.add("is-visible");
    }
    return;
  }

  var reveal = new IntersectionObserver(
    function (records) {
      records.forEach(function (record) {
        if (!record.isIntersecting) return;
        record.target.classList.add("is-visible");
        reveal.unobserve(record.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
  );

  for (var j = 0; j < entries.length; j++) {
    // Stagger the first few; beyond that the delay stops accumulating.
    entries[j].style.transitionDelay = Math.min(j * 90, 360) + "ms";
    reveal.observe(entries[j]);
  }
})();

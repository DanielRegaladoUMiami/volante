/* Volante — interactive flat-fare + savings estimator (no backend).
   Pure client-side: pick where you're out + where home is → instant estimated
   flat fare and how it compares to a surged Uber + leaving your car behind.
   Estimates are illustrative / pre-launch, NOT validated prices. */
(function () {
  "use strict";

  // Rough relative positions on a local grid where ~1 unit ≈ 1 mile (Miami-ish).
  var ZONES = {
    "Brickell":        [0, 0],
    "Downtown":        [0, 1.2],
    "Edgewater":       [0, 2.2],
    "Wynwood":         [0.3, 3.2],
    "Midtown":         [0.4, 3.0],
    "Little Havana":   [-2, 0.4],
    "Coconut Grove":   [-1, -4],
    "Coral Gables":    [-3.5, -3],
    "South Beach":     [4, 2.2],
    "Mid-Beach":       [5, 4.6],
    "Key Biscayne":    [3, -3],
    "Aventura":        [2.5, 12],
    "Doral":           [-9, 1.5],
    "Kendall":         [-8, -9],
    "Homestead":       [-10, -22]
  };

  function miles(a, b) {
    var A = ZONES[a], B = ZONES[b];
    if (!A || !B) return null;
    return Math.hypot(A[0] - B[0], A[1] - B[1]);
  }

  // Flat per-trip estimate. Illustrative pre-launch formula, not a validated price.
  function estimateFare(pickup, dropoff) {
    var mi = miles(pickup, dropoff);
    if (mi === null) return null;
    var fare = Math.max(45, 32 + 6 * mi);
    return Math.round(fare / 5) * 5; // nearest $5
  }

  // Rough "what the alternative costs you" — surged rideshare there + Uber back tomorrow for the car.
  function alternativeCost(pickup, dropoff) {
    var mi = miles(pickup, dropoff);
    if (mi === null) return null;
    var oneWaySurge = Math.round((4 + 1.7 * mi) * 2.4); // club-night surge
    var nextDayBack = Math.round(4 + 1.7 * mi);          // trip back for the car
    return { surge: oneWaySurge, back: nextDayBack, total: oneWaySurge + nextDayBack };
  }

  var STR = {
    es: {
      fareLabel: "Tu tarifa fija estimada",
      est: "estimada · piloto, sin validar",
      altHead: "¿Y un Uber?",
      altSurge: "Con surge esa noche — pero te deja sin tu carro:",
      back: "Vuelves por él mañana",
      tow: "O grúa en South Beach",
      dui: "O un DUI",
      keep: "Volante: una tarifa fija y tu carro amanece contigo en casa.",
      pickFirst: "Elige de dónde sales y a dónde vas a casa.",
      same: "Mismo barrio — tarifa mínima."
    },
    en: {
      fareLabel: "Your estimated flat fare",
      est: "estimate · pilot, unvalidated",
      altHead: "What about an Uber?",
      altSurge: "Surged that night — but it leaves you without your car:",
      back: "Go back for it tomorrow",
      tow: "Or a South Beach tow",
      dui: "Or a DUI",
      keep: "Volante: one flat fare and your car is home with you by morning.",
      pickFirst: "Pick where you're out and where home is.",
      same: "Same area — minimum fare."
    }
  };

  function money(n) { return "$" + n; }

  function init() {
    var root = document.getElementById("estimator");
    if (!root) return;
    var lang = root.getAttribute("data-lang") === "en" ? "en" : "es";
    var t = STR[lang];

    var pickup = document.getElementById("est-pickup");
    var dropoff = document.getElementById("est-dropoff");
    var fareEl = document.getElementById("est-fare");
    var fareNote = document.getElementById("est-fare-note");
    var compareEl = document.getElementById("est-compare");
    var keepEl = document.getElementById("est-keep");

    // hidden fields synced into the request form
    var hPickup = document.getElementById("f-pickup");
    var hDropoff = document.getElementById("f-dropoff");
    var hEstimate = document.getElementById("f-estimate");

    function render() {
      var p = pickup.value, d = dropoff.value;
      if (!p || !d) {
        fareEl.textContent = "—";
        fareNote.textContent = t.pickFirst;
        compareEl.innerHTML = "";
        keepEl.textContent = "";
        if (hEstimate) hEstimate.value = "";
        return;
      }
      var fare = estimateFare(p, d);
      var alt = alternativeCost(p, d);
      fareEl.textContent = money(fare);
      fareNote.textContent = t.est + (p === d ? " · " + t.same : "");
      compareEl.innerHTML =
        '<div class="est-compare-head">' + t.altHead + ' <span>~' + money(alt.surge) + '</span></div>' +
        '<div class="est-compare-sub">' + t.altSurge + '</div>' +
        '<div class="est-row"><span>' + t.back + '</span><span>~' + money(alt.back) + '</span></div>' +
        '<div class="est-row"><span>' + t.tow + '</span><span>$516</span></div>' +
        '<div class="est-row est-total"><span>' + t.dui + '</span><span>~$10,000</span></div>';
      keepEl.innerHTML = "🚗 " + t.keep;

      if (hPickup) hPickup.value = p;
      if (hDropoff) hDropoff.value = d;
      if (hEstimate) hEstimate.value = String(fare);
    }

    pickup.addEventListener("change", render);
    dropoff.addEventListener("change", render);
    render();

    // Request submit → Google Sheet (same endpoint as the waitlist), framed as a pilot request.
    var form = document.getElementById("request-form");
    var flash = document.getElementById("req-flash");
    if (!form) return;
    var OK = lang === "en"
      ? "Saved! You're on the pilot list — we'll reach out on WhatsApp. 🚗"
      : "¡Listo! Estás en la lista del piloto — te escribimos por WhatsApp. 🚗";
    var ERR = lang === "en" ? "Something went wrong. Try again." : "Algo salió mal. Inténtalo de nuevo.";
    var SOON = lang === "en"
      ? "Coming soon! (Google Sheet isn't connected yet.)"
      : "¡Pronto! (falta conectar la hoja de Google.)";

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!pickup.value || !dropoff.value) { render(); return; }
      flash.className = "flash";
      if (form.action.indexOf("__SHEET_WEBAPP_URL__") !== -1) {
        flash.className = "flash flash-ok"; flash.textContent = SOON; return;
      }
      fetch(form.action, { method: "POST", mode: "no-cors", body: new URLSearchParams(new FormData(form)) })
        .then(function () { form.reset(); render(); flash.className = "flash flash-ok"; flash.textContent = OK; })
        .catch(function () { flash.className = "flash flash-err"; flash.textContent = ERR; });
    });
  }

  // Expose the pure fns for tests (Node).
  if (typeof module !== "undefined" && module.exports) {
    module.exports = { estimateFare: estimateFare, alternativeCost: alternativeCost, miles: miles, ZONES: ZONES };
  } else {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
  }
})();

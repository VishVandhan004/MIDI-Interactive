const pianoKeys = document.querySelectorAll(".piano-keys .key"),
      instrumentDropdown = document.getElementById("instrumentDropdown");

// send instrument change to Flask
instrumentDropdown.addEventListener("change", e => {
  fetch("/set_instrument", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ instrument: e.target.value })
  });
});

// helper to map data-key → note_name (sa, re, …)
function dataKeyToNoteName(key) {
  // your mapping from data-key attributes to midi_logic keys
  const map = { a: "sa", w: "re", s: "ga", e: "ma", d: "pa", t: "dha", g: "ni", y: "sa_high" };
  return map[key];
}

// when mouse-down (or touch) on a key
pianoKeys.forEach(key => {
  key.addEventListener("mousedown", () => {
    const note = dataKeyToNoteName(key.dataset.key);
    if (note) fetch(`/play_note/${note}`);
  });
  key.addEventListener("mouseup", () => {
    const note = dataKeyToNoteName(key.dataset.key);
    if (note) fetch(`/stop_note/${note}`);
  });
});

// also allow keyboard-press to click keys visually & send to Flask
document.addEventListener("keydown", e => {
  const keyEl = document.querySelector(`.key[data-key="${e.key}"]`);
  if (!keyEl) return;
  keyEl.classList.add("active");
  const note = dataKeyToNoteName(e.key);
  if (note) fetch(`/play_note/${note}`);
});
document.addEventListener("keyup", e => {
  const keyEl = document.querySelector(`.key[data-key="${e.key}"]`);
  if (!keyEl) return;
  keyEl.classList.remove("active");
  const note = dataKeyToNoteName(e.key);
  if (note) fetch(`/stop_note/${note}`);
});

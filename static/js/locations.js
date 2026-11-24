/* ============================================================
   locations.js — State of Origin  ➜  Local Government
   ------------------------------------------------------------
   WHAT'S DONE FOR YOU:
     • Grabbing the two <select> elements.
     • A helper to (re)fill a select with [{id?, name}] options.
     • The change-listener that resets the LGA list when the
       state changes.

   WHAT YOU IMPLEMENT (look for "TODO"):
     1. Fetch the list of states when the page loads, then call
        fillSelect(stateSelect, states).
     2. When a state is chosen, fetch that state's LGAs, then call
        fillSelect(lgaSelect, lgas).

   The brief requires this to be ASYNCHRONOUS. Use fetch() + then/
   catch, or async/await. Two common ways to get the data:
       (a) hit your own Flask JSON endpoints, e.g.
             GET /api/states            -> ["Abia State", ...]
             GET /api/lgas/<state>      -> ["Aba North", ...]
       (b) fetch the bundled file static/data/states-lgas.json
           (shape: [{ "state": "...", "local": ["...", ...] }, ...])
           and filter it in the browser.
   Pick one and delete the other TODO.
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
  const stateSelect = document.getElementById("state");
  const lgaSelect = document.getElementById("lga");
  if (!stateSelect || !lgaSelect) return;

  // Refill a <select>, keeping its first (placeholder) option.
  function fillSelect(select, items, placeholder) {
    select.length = 1;                       // drop everything except the placeholder
    if (placeholder) select.options[0].text = placeholder;
    items.forEach(function (item) {
      const value = typeof item === "string" ? item : (item.id ?? item.name);
      const label = typeof item === "string" ? item : item.name;
      select.add(new Option(label, value));
    });
  }

  // ---- TODO 1: load the states on page load -------------------
  // Example skeleton (fill in the fetch):
  //
    fetch("/api/states")
      .then(function (res) { return res.json(); })
      .then(function (states) { fillSelect(stateSelect, states); })
      .catch(function (err) { console.error("Could not load states", err); });
  //
  // (Remove this comment block once implemented.)

  // ---- LGA reset + load when the state changes ----------------
  stateSelect.addEventListener("change", function () {
    fillSelect(lgaSelect, [], "Loading…");   // visual reset while you fetch

    const chosenState = this.value;

    // ---- TODO 2: load LGAs for `chosenState` ------------------
    // Example skeleton:
    //
      fetch("/api/lgas/" + encodeURIComponent(chosenState))
        .then(function (res) { return res.json(); })
        .then(function (lgas) { fillSelect(lgaSelect, lgas, "Select Local Government"); })
        .catch(function (err) {
          console.error("Could not load LGAs", err);
          fillSelect(lgaSelect, [], "Select Local Government");
        });
  });
});

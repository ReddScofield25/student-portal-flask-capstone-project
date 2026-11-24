/* ============================================================
   status.js — change a student's admission status WITHOUT reload
   ------------------------------------------------------------
   WHAT'S DONE FOR YOU:
     • Reading the student id from the <select data-student-id>.
     • A change-listener and a small helper to show feedback text
       and update the visible status on the page.

   WHAT YOU IMPLEMENT (look for "TODO"):
     • POST the new status to your backend asynchronously and,
       on success, reflect it in the UI. No page reload.

   Suggested backend contract:
       POST /update_status
       body (JSON or form): { student_id: <id>, status: <value> }
       response: 200 on success, 400 on an invalid status.
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
  const select = document.getElementById("status-select");
  if (!select) return;

  const studentId = select.dataset.studentId;
  const feedback = document.getElementById("status-feedback");
  const currentStatus = document.getElementById("current-status");

  function showFeedback(message, ok) {
    if (!feedback) return;
    feedback.textContent = message;
    feedback.style.color = ok ? "#1E9E5A" : "#C0392B";
  }

  // Keep the pills/labels in sync once the server confirms the change.
  function reflectStatus(newStatus) {
    if (currentStatus) currentStatus.textContent = newStatus;
    document.querySelectorAll(".pill").forEach(function (pill) {
      pill.className = "pill " + newStatus;
      pill.textContent = newStatus;
    });
  }

  select.addEventListener("change", function () {
    const newStatus = this.value;
    if (!newStatus) return;
    showFeedback("Saving…", true);

    // ---- TODO: send the change asynchronously ------------------
    // Example skeleton (fill in the fetch):
    //
      fetch("/update_status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: studentId, status: newStatus })
      })
        .then(function (res) {
          if (!res.ok) throw new Error("Request failed");
          return res.json();
        })
        .then(function () {
          reflectStatus(newStatus);
          showFeedback("Saved ✓", true);
        })
        .catch(function (err) {
          console.error(err);
          showFeedback("Could not save", false);
        });
    //
    // (Remove this comment block once implemented.)
  });
});

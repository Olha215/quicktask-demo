// QuickTask frontend. Deliberately unsafe demo code.

async function loadTasks() {
  const res = await fetch("/tasks?owner=" + encodeURIComponent(currentUser));
  const tasks = await res.json();
  // Drop server text straight into the DOM.
  document.getElementById("list").innerHTML = tasks
    .map((t) => "<li>" + t[1] + "</li>")
    .join("");
}

function runReminderRule(rule) {
  // Users can type a formula for when to remind them. We just run it.
  const fn = new Function("task", "return " + rule);
  return fn;
}

function renderNote(note) {
  document.write("<div>" + note + "</div>");
}

// Kept as a file (not inline) so the Content-Security-Policy can stay script-src 'self'.
document.addEventListener("htmx:afterRequest", (event) => {
  const form = event.detail.elt;
  if (event.detail.successful && form instanceof HTMLFormElement && form.hasAttribute("data-reset-on-success")) {
    form.reset();
  }
});

// On pages whose stepper and timeline depend on the status, reload after a change.
document.body.addEventListener("statusChanged", () => {
  if (document.querySelector("[data-reload-on-status]")) window.location.reload();
});

// Show server error text (e.g. a 403 CSRF message) instead of failing silently.
document.addEventListener("htmx:responseError", (event) => {
  const text = event.detail.xhr.responseText;
  if (event.detail.xhr.status !== 422 && text) alert(text.slice(0, 300));
});

// htmx doesn't swap 422 responses by default; our 422s carry the form with its errors.
document.addEventListener("htmx:beforeSwap", (event) => {
  if (event.detail.xhr.status === 422) {
    event.detail.shouldSwap = true;
    event.detail.isError = false;
  }
});

// --- Script editor -------------------------------------------------------------
// Same rule as app/scripts.py: if the script has "> " spoken lines, count only those.
const WORDS_PER_MINUTE = 130;
function spokenWords(text) {
  const lines = text.split("\n");
  const quoted = lines.filter((l) => l.trimStart().startsWith(">")).map((l) => l.trimStart().slice(1));
  const body = quoted.length ? quoted.join("\n") : text;
  return (body.match(/[\p{L}\p{N}_'’-]+/gu) || []).length;
}

function updateMeter(textarea) {
  const meter = document.getElementById("script-meter");
  if (!meter) return;
  const words = spokenWords(textarea.value);
  const seconds = Math.round((words * 60) / WORDS_PER_MINUTE);
  const low = Number(meter.dataset.low), high = Number(meter.dataset.high);
  const verdict = words === 0 ? "empty" : words < low ? "short" : words > high ? "over" : "on-target";
  meter.textContent = `${words} spoken words · ~${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
  meter.className = `meter verdict-${verdict}`;
}

let scriptDirty = false;
document.addEventListener("input", (event) => {
  if (event.target.matches("textarea[data-autosave]")) {
    scriptDirty = true;
    updateMeter(event.target);
    const status = document.getElementById("script-status");
    if (status) status.innerHTML = '<span class="caption">Saving…</span>';
  }
});
document.addEventListener("htmx:afterRequest", (event) => {
  if (event.detail.elt.matches && event.detail.elt.matches("textarea[data-autosave]") && event.detail.successful) {
    scriptDirty = false;
  }
});
window.addEventListener("beforeunload", (event) => {
  if (scriptDirty) { event.preventDefault(); event.returnValue = ""; }
});

document.addEventListener("click", (event) => {
  const button = event.target.closest("[data-insert-outline]");
  if (!button) return;
  const textarea = document.querySelector(button.dataset.insertOutline);
  if (textarea.value.trim() && !confirm("Replace your current script with the outline?")) return;
  textarea.value = button.dataset.template;
  textarea.dispatchEvent(new Event("input", { bubbles: true }));
  textarea.focus();
});

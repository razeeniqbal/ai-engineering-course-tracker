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

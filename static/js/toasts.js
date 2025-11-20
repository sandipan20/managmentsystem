function showToast(title, body, autohide=true){
  const id = 'toast-'+Math.random().toString(36).slice(2,9);
  const container = document.getElementById('toast-container');
  if(!container) return;
  const el = document.createElement('div');
  el.className = 'toast align-items-center text-bg-dark border-0 mb-2';
  el.id = id;
  el.setAttribute('role','alert');
  el.setAttribute('aria-live','assertive');
  el.setAttribute('aria-atomic','true');
  el.innerHTML = `
    <div class="d-flex">
      <div class="toast-body"> <strong>${title}</strong><div class="small">${body}</div></div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
  `;
  container.appendChild(el);
  const bsToast = new bootstrap.Toast(el, {autohide: autohide, delay: 3000});
  bsToast.show();
  el.addEventListener('hidden.bs.toast', ()=> el.remove());
  return bsToast;
}

// expose globally
window.showToast = showToast;

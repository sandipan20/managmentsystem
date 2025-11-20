document.addEventListener('DOMContentLoaded', ()=>{
  // Register form submit
  const regBtn = document.getElementById('register-submit');
  const regForm = document.getElementById('register-form');
  if(regBtn && regForm){
    regBtn.addEventListener('click', async ()=>{
      const fd = new FormData(regForm);
      const body = {};
      for(const [k,v] of fd.entries()) body[k]=v;
      const res = await fetch('/register', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
      if(res.ok){
        const data = await res.json();
        showToast('Registered', `Student ${data.name} created`);
        // close modal
        const modalEl = document.getElementById('registerModal');
        const bs = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
        bs.hide();
        // optional: reload students list page if on it
        if(location.pathname.startsWith('/students')) location.reload();
      } else {
        const err = await res.json().catch(()=>({error:'error'}));
        showToast('Error', err.error || 'Unable to register');
      }
    });
  }

  // Delete student buttons (delegate)
  document.body.addEventListener('click', async (e)=>{
    const btn = e.target.closest('.delete-student-btn');
    if(!btn) return;
    const sid = btn.datasetId || btn.getAttribute('data-id') || btn.dataset.id;
    if(!sid) return;
    if(!confirm('Delete student? This cannot be undone.')) return;
    const res = await fetch(`/students/${sid}/delete`, {method:'POST'});
    if(res.ok){
      showToast('Deleted', 'Student removed');
      // remove element from DOM if present
      const item = btn.closest('.list-group-item') || btn.closest('tr');
      if(item) item.remove();
    } else {
      const err = await res.json().catch(()=>({error:'error'}));
      showToast('Error', err.error || 'Unable to delete');
    }
  });
});

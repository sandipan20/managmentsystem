document.addEventListener('DOMContentLoaded', function(){
  const sid = window.SID;
  const form = document.getElementById('student-form');
  const status = document.getElementById('save-status');
  const instForm = document.getElementById('installment-form');
  const instList = document.getElementById('installments-list');

  async function fetchStudent(){
    const res = await fetch(`/api/students/${sid}`);
    const data = await res.json();
    renderInstallments(data.installments || []);
    // update fee summaries
    const totalFeeEl = document.getElementById('total-fee');
    const totalPaidEl = document.getElementById('total-paid');
    const remainingEl = document.getElementById('remaining-fee');
    if(totalFeeEl && typeof data.total_fee !== 'undefined') totalFeeEl.textContent = parseFloat(data.total_fee).toFixed(2);
    if(totalPaidEl && typeof data.total_paid !== 'undefined') totalPaidEl.textContent = parseFloat(data.total_paid).toFixed(2);
    if(remainingEl){
      if(typeof data.remaining_fee !== 'undefined') remainingEl.textContent = parseFloat(data.remaining_fee).toFixed(2);
      else if(typeof data.total_fee !== 'undefined' && typeof data.total_paid !== 'undefined') remainingEl.textContent = (parseFloat(data.total_fee)-parseFloat(data.total_paid)).toFixed(2);
    }
    // update points display
    const pts = document.getElementById('student-points');
    if(pts) pts.textContent = data.points || 0;
    // update badges list if any
    if(data.installments && Array.isArray(data.installments)){
      // no-op here; badges are loaded on page render
    }
  }

  function renderInstallments(list){
    instList.innerHTML = '';
    list.forEach((ins, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${idx+1}</td>
        <td>${ins.amount}</td>
        <td>${ins.due_date ? ins.due_date.split('T')[0] : ''}</td>
        <td>${ins.paid_date ? ins.paid_date.split('T')[0] : ''}</td>
        <td>${ins.status}</td>
        <td>
          <button class="btn btn-sm btn-success mark-paid" data-id="${ins.id}">Mark Paid</button>
          <button class="btn btn-sm btn-danger delete-ins" data-id="${ins.id}">Delete</button>
        </td>
      `;
      instList.appendChild(tr);
    });
    // attach handlers
    document.querySelectorAll('.mark-paid').forEach(btn => {
      btn.addEventListener('click', async (e)=>{
        const id = e.target.dataset.id;
        await fetch(`/api/installments/${id}`, {method:'PUT', headers:{'content-type':'application/json'}, body: JSON.stringify({status:'paid'})});
        fetchStudent();
      })
    });

    // delete uses modal confirmation
    document.querySelectorAll('.delete-ins').forEach(btn => {
      btn.addEventListener('click', (e)=>{
        const id = e.target.dataset.id;
        showDeleteModal(id);
      })
    });
  }

  form.addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const fd = new FormData(form);
    const body = {};
    for(const [k,v] of fd.entries()) body[k]=v;
    status.textContent = 'Saving...';
    const res = await fetch(`/api/students/${sid}`, {method:'PUT', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
    if(res.ok){
      status.textContent = 'Saved';
      showToast('Saved', 'Student details updated');
      setTimeout(()=> status.textContent = '', 2000);
      // refresh summary values
      fetchStudent();
    } else {
      status.textContent = 'Error saving';
      showToast('Error', 'Unable to save student details');
    }
  });

  instForm.addEventListener('submit', async (ev)=>{
    ev.preventDefault();
    const fd = new FormData(instForm);
    const body = {};
    for(const [k,v] of fd.entries()) body[k]=v;
    const res = await fetch(`/api/students/${sid}/installments`, {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
    if(res.ok){
      instForm.reset();
      fetchStudent();
    }
  });

  // quick award points button
  const giveBtn = document.getElementById('give-points-btn');
  if(giveBtn){
    giveBtn.addEventListener('click', async ()=>{
      const res = await fetch(`/api/students/${sid}/points`, {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({points:5})});
      if(res.ok){
        const data = await res.json();
        const pts = document.getElementById('student-points');
        if(pts) pts.textContent = data.points;
        // simple animation
        giveBtn.classList.add('btn-success');
        setTimeout(()=> giveBtn.classList.remove('btn-success'), 800);
      }
    });
  }

  // initialize flatpickr on due_date inputs
  try{
    if(window.flatpickr){
      flatpickr('input[name="due_date"]', {dateFormat:'Y-m-d'});
    }
  }catch(e){ }

  // delete modal flow
  let pendingDeleteId = null;
  const deleteModal = document.getElementById('confirmDeleteModal');
  const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
  function showDeleteModal(id){
    pendingDeleteId = id;
    const modal = new bootstrap.Modal(deleteModal);
    modal.show();
  }
  if(confirmDeleteBtn){
    confirmDeleteBtn.addEventListener('click', async ()=>{
      if(!pendingDeleteId) return;
      await fetch(`/api/installments/${pendingDeleteId}`, {method:'DELETE'});
      pendingDeleteId = null;
      var modalEl = bootstrap.Modal.getInstance(deleteModal);
      if(modalEl) modalEl.hide();
      fetchStudent();
    });
  }

  // initial load
  fetchStudent();
});

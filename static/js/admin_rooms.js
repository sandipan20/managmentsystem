document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.room-card').forEach(card=>{
    const btn = card.querySelector('.room-btn');
    const details = card.querySelector('.room-details');
    let expanded = false;
    btn.addEventListener('click', async ()=>{
      const roomId = card.dataset.roomId;
      if(!expanded){
        // fetch students in room
        const res = await fetch(`/api/rooms/${roomId}/students`);
        if(res.ok){
          const data = await res.json();
          if(data.items && data.items.length){
            details.innerHTML = '<ul class="list-group">' + data.items.map(s=>`<li class="list-group-item"><strong>${s.name}</strong> (${s.roll_no})<br/><small>${s.email} • ${s.phone || ''}</small></li>`).join('') + '</ul>';
          } else {
            details.innerHTML = '<div class="text-muted">No students allocated</div>';
          }
        } else {
          details.innerHTML = '<div class="text-danger">Error loading</div>';
        }
        details.style.display = 'block';
        expanded = true;
      } else {
        details.style.display = 'none';
        expanded = false;
      }
    });
  });
});

// Small UI helpers for the new frontend
document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('global-search');
  const searchBtn = document.getElementById('search-btn');
  if (searchBtn && searchInput) {
    searchBtn.addEventListener('click', function () {
      const q = searchInput.value.trim();
      if (!q) return;
      // basic redirect to students search (server handles query param)
      window.location.href = '/students?q=' + encodeURIComponent(q);
    });
    searchInput.addEventListener('keyup', function (e) {
      if (e.key === 'Enter') searchBtn.click();
    });
  }

  // Simple mobile behavior: focus search when hitting '/'
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
      if (searchInput) { searchInput.focus(); e.preventDefault(); }
    }
  });
});

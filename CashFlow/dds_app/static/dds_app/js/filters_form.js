document.addEventListener('DOMContentLoaded', function() {
  const resetBtn = document.getElementById('resetFilters');
  const filterForm = document.getElementById('filterForm');
  
  resetBtn.addEventListener('click', function(e) {
    e.preventDefault();
    
    const inputs = filterForm.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
      if (input.tagName === 'SELECT') {
        input.selectedIndex = 0;
      } 
      else if (input.type === 'text' || input.type === 'date' || input.type === 'number') {
        input.value = '';
      }
      else if (input.type === 'checkbox' || input.type === 'radio') {
        input.checked = false;
      }
    });
    
    filterForm.submit();
  });
});
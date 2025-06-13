const ctx = document.getElementById('myChart');

  new Chart(ctx, {
      type: 'pie',
      data: {
        labels: [
          'Red',
          'Blue',
          'Yellow'
        ],
        datasets: [{
          label: 'Сумма',
          data: [300, 50, 100],
          hoverOffset: 4
        }]
    }
  });
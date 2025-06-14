const ctx = document.getElementById('myChart');
const chart_data = document.getElementById('chart-data');
let keys = [], values = [];

Array.from(chart_data.children).forEach(child => {
  keys.push(child.getAttribute('key'));
  values.push(parseInt(child.getAttribute('value')));
});

new Chart(ctx, {
    type: 'pie',
    data: {
      labels: keys,
      datasets: [{
        label: 'Сумма',
        data: values,
        hoverOffset: 4
      }]
  }
});
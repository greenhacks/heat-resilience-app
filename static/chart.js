'use strict';



fetch('/alerts.json')
.then(response => response.json())
.then(responseJson => {
  const data = responseJson.data.map(dailyTotal => ({
    x: dailyTotal.date, y: dailyTotal.melons_sold,
  }));
  new Chart(document.querySelector('#line-time'), {
    type: 'line',
    data: {
      datasets: [{
        label: 'All Melons', data,  // equivalent to data: data
      }],
    },
    options: {
      scales: {
        x: {
          type: 'time',
          time: {
            tooltipFormat: 'LLLL dd', unit: 'day',
          },
      }},
    },
  });
});
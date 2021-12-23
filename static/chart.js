'use strict';

// new Chart(document.querySelector('#alert-chart'), {
//   type: 'bar',
//   data: {
//     labels: ['Watermelon', 'Cantaloupe', 'Honeydew'],
//     datasets: [
//       {
//         label: 'Today',
//         data: [10, 36, 27],
//       },
//       {
//         label: 'Yesterday',
//         data: [5, 0, 7],
//       },
//     ],
//   },
// });

// fetch('/sales_this_week.json')
// .then(response => response.json())
// .then(responseJson => {
//   const data = responseJson.data.map(dailyTotal => ({
//     x: dailyTotal.date, y: dailyTotal.melons_sold,
//   }));
//   new Chart(document.querySelector('#line-time'), {
//     type: 'line',
//     data: {
//       datasets: [{
//         label: 'All Melons', data,  // equivalent to data: data
//       }],
//     },
//     options: {
//       scales: {
//         x: {
//           type: 'time',
//           time: {
//             tooltipFormat: 'LLLL dd', unit: 'day',
//           },
//       }},
//     },
//   });
// });
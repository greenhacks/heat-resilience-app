'use strict';


fetch('/monthly-alerts.json')
 .then(response => response.json())
 .then(responseJson => {
    const data = responseJson.data.map(monthlyTotal => (
        
        {x: monthlyTotal.month, 
        y: monthlyTotal.alerts}
        
        ));
    console.log(responseJson)

    //Line chart using Chart.js
    // grid configuiration
    const DISPLAY = true;
    const BORDER = true;
    const CHART_AREA = true;
    const TICKS = true;


    const lineChart = new Chart(document.querySelector('#line-chart'),
        {
        type: 'line',
        indexAxis: 'x',
        data: {
            labels: ['January', 'February', 'March', 'April', 'May',
                    'June', 'July', 'August', 'September', 'October', 
                    'November', 'December'],
            datasets: [{
                label: 'Alerts', data,
                size: 10,
                fill: false,
                borderColor: 'rgb(207, 92, 54)',
                tension: 0.1,
                radius: 1,
                borderWidth: 4,
                borderJoinStyle: 'miter',
            }]
        }, 
        options: {
          plugins: {
            legend: {
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 20, 
                    },
                    color: 'black'
                }
            }
        },
            scales: {
              x: {
                grid: {
                  display: false,
                  drawBorder: BORDER,
                  drawOnChartArea: CHART_AREA,
                  drawTicks: TICKS,
                  color: 'black'
                },
                ticks: {
                  color: 'black'
                }, 
                title: {
                  font: {
                    size: 20
                  },
                  size: 100,
                  color: 'black',
                  display: true,
                  text: 'Month',
                  textSize: 100
                }
              }, 
              y: {
                grid: {
                  color: 'black',
                  display: DISPLAY,
                  drawBorder: BORDER,
                  drawOnChartArea: CHART_AREA,
                  drawTicks: TICKS,
                },
                ticks: {
                  color: 'black',
                  size: 20
                }, 
                title: {
                  font: {
                    size: 20
                  },
                  padding: {top: 0, left: 0, right: 30, bottom: 0},
                  color: 'black',
                  display: true,
                  text: 'Text Alerts',
                  textSize: 100
                }
              }
            }
          }
        }
    )
});
'use strict';

fetch('/monthly-alerts.json')
 .then(response => response.json())
 .then(responseJson => {
    const data = responseJson.data.map(monthlyTotal => (
        
        {x: monthlyTotal.month, y: monthlyTotal.alerts}
        
        ));
    console.log(responseJson)

    //Line chart
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
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
            }]
        }
        }
    )});
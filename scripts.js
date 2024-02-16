let selectedOptions = {};
let chart = null;
function selectOption(event, option) {
    event.preventDefault();
    fetchData().then(data => {
        if (data[option]) {
            updateChart(data, option);
        }
    });
}

async function fetchData() {
    const response = await fetch('http://127.0.0.1:5000/data');
    const data = await response.json();
    return data; // Ensure this matches the new format
}

async function updateChart(data, option) {
    const ctx = document.getElementById('myChart').getContext('2d');
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[option].x, // x-coordinates
            datasets: [{
                label: option,
                data: data[option].y, // y-coordinates
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
    options: {
        responsive: true, // Ensures the chart is responsive
        maintainAspectRatio: false, // Ensures the chart fills the container
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'lightgrey' // Sets the grid lines to white
                },
                ticks: {
                    color: 'black', // Sets the ticks to white
                }
            },
            x: {
                grid: {
                    color: 'lightgrey' // Sets the grid lines to white
                },
                ticks: {
                    color: 'black' // Sets the ticks to white
                },
                title: {
                    display: true,
                    text: 'Duration',
                    color: 'white', // Title color
                    font: {
                        size: 12, // Smaller font size
                        weight: 'bold' // Bold font weight
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: false // Hides the legend
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        label += `${context.parsed.y}%`;
                        return label;
                    }
                }
            }
        }
    }
});
}

    function startTableDataFetch() {
        console.log("Setting up table data fetch interval");
        setInterval(async () => {
            console.log("Fetching table data...");
            await populateTable();
        }, 60000); // Adjusted to 60,000 ms (1 minute)
    }

    function startInflationDataFetch() {
        console.log("Setting up inflation data fetch interval");
        setInterval(async () => {
            console.log("Fetching inflation data...");
            await updateInflationChart();
        }, 60000);
    }

    function startForwardRatesFetch() {
        console.log("Setting up forward rates fetch interval");
        setInterval(async () => {
            console.log("Fetching forward rates data...");
            await updateforward('forward_rate'); // Adjust the argument as necessary
        }, 60000);
    }

let isFetchingTableData = false;
let isFetchingInflationData = false;
let isFetchingForwardRates = false;

async function populateTable() {
    if (isFetchingTableData) {
        console.log("Already fetching table data. Skipping...");
        return;
    }
    isFetchingTableData = true;
    console.log("Fetching table data...");
    const tableDataResponse = await fetch('http://127.0.0.1:5000/table_data');
    const tableData = await tableDataResponse.json();
    const table = document.getElementById('myTable').getElementsByTagName('tbody')[0];

    // Clear existing rows
    table.innerHTML = '';

    // Populate the table with data
    tableData.forEach(item => {
    const row = table.insertRow();

    // Create a cell for each key-value pair in the item object
    Object.values(item).forEach(value => {
        const cell = row.insertCell();
        cell.innerHTML = value;
        // Optionally, you can add a class to cells if you want to apply specific styles
        cell.classList.add('cell-style');
    });
    });
    isFetchingTableData = false;
}

// Call the populateTable function to fetch and display the table data
populateTable();

async function fetchInflationData() {
    const response = await fetch('http://127.0.0.1:5000/verdbolgualag');
    return await response.json();
}
async function fetchforward() {
    const response = await fetch('http://127.0.0.1:5000/framvirkir-vextir');
    return await response.json();
}
const chartColors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF', '#7BC225'];

async function updateforward(rateType) {
    if (isFetchingForwardRates) {
        console.log(`Already fetching ${rateType} data. Skipping...`);
        return;
    }
    isFetchingForwardRates = true;
    console.log(`Fetching ${rateType} data...`);
    const response = await fetch(`http://127.0.0.1:5000/${rateType}`);
    const overdData = await response.json();

    const datasets = [];
    let colorIndex = 0;
    for (const key in overdData) {
        const dataPoints = overdData[key].map(item => {
            return { x: item[0], y: item[1] };
        });

        const color = chartColors[colorIndex % chartColors.length]; // Cycle through the colors
        datasets.push({
            label: key,
            data: dataPoints,
            fill: false,
            borderColor: color, // Use predefined color
            pointRadius: 5,
            pointHoverRadius: 7
        });
        colorIndex++; // Move to the next color
    }
    

    const ctx = document.getElementById('forward-rates').getContext('2d');
    if (window.forwardRatesChart) {
        window.forwardRatesChart.destroy();
    }
    window.forwardRatesChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: datasets
        },
        options: {
            responsive: true,
            animation: false,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    title: {
                        display: true,
                        text: 'Duration',
                        color: "white"
                    }
                },
                y: {
                    title: {
                        display: false,
                        text: 'Forward Rate (%)',
                        color: "white"
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.parsed.y}%`;
                        }
                    }
                }
            }
        }
    });
    isFetchingForwardRates = true;
}

updateforward('forward_rate');

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

async function updateInflationChart() {
    if (isFetchingInflationData) {
        console.log("Already fetching inflation data. Skipping...");
        return;
    }
    isFetchingInflationData = true;
    console.log("Fetching inflation data...");
    const response = await fetch('http://127.0.0.1:5000/verdbolgualag');
    const data = await response.json();

    const datasetHnit2 = data.hnit2.map(item => {
        return { x: item[1], y: item[2], name: item[0] };
    });

    const ctx = document.getElementById('inflationChart').getContext('2d');
    const inflationChart = new Chart(ctx, {
        type: 'scatter',  // Change to scatter for individual points
        data: {
            datasets: [
                {
                    label: 'Verdbolgualag',
                    data: data.hnit.map(item => ({ x: item[0], y: item[1] })),
                    borderColor: 'rgb(75, 192, 192)',
                    fill: false,
                    showLine: true,  // Connects the points with a line
                },
                {
                    label: 'Bref',
                    data: datasetHnit2,
                    borderColor: 'rgb(192, 75, 75)',
                    backgroundColor: 'rgb(192, 75, 75)',
                    fill: false,
                    showLine: false,  // No line between points
                    pointRadius: 5,
                    pointHoverRadius: 7,
                }
            ]
        },
    options: {
        responsive: true, // Ensures the chart is responsive
        maintainAspectRatio: false, // Ensures the chart fills the container
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'grey' // Sets the grid lines to white
                },
                ticks: {
                    color: 'white', // Sets the ticks to white
                    callback: function(value) {
                        return value + '%'; // Formats as percentage
                    }
                },
                title: {
                    display: false,
                    text: 'Percentage',
                    color: 'white' // Title color
                }
            },
            x: {
                grid: {
                    color: 'grey' // Sets the grid lines to white
                },
                ticks: {
                    color: 'white' // Sets the ticks to white
                },
                title: {
                    display: true,
                    text: 'Duration',
                    color: 'white', // Title color
                    font: {
                        size: 12, // Smaller font size
                        weight: 'bold' // Bold font weight
                    }
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        var label = context.dataset.label || '';

                        if (label === 'Bref') {
                            // Access the custom name property from the context's raw data
                            return context.raw.name + ': (' + context.label + ', ' + context.formattedValue + '%)';
                        } else {
                            return label + ': ' + context.formattedValue + '%';
                        }
                    }
                },
            legend: {
                display: true, // Hides the legend
                labels:{
                    color:"white"
                }
            }
        }
    }
}
});
isFetchingInflationData = false;
}
// Call the function to plot the inflation data
updateInflationChart();

document.querySelectorAll('#dropdown-top-left .dropdown-content a').forEach(item => {
    item.addEventListener('click', function(event) {
        selectOption(event, event.target.textContent.trim());
    });
});

document.addEventListener('DOMContentLoaded', (event) => {
    // This will run when the document is loaded
    let isFullscreen = false; // State to track fullscreen status
    startTableDataFetch();
    startInflationDataFetch();
    startForwardRatesFetch();
    function toggleFullscreen(elem) {
        // Toggle the fullscreen class
        elem.classList.toggle('fullscreen');
        isFullscreen = !isFullscreen; // Update the state
    }
    

    // Add click event listeners to each graph container
    document.querySelectorAll('#graph-top-left, #graph-top-right, #graph-bottom-right').forEach((graph) => {
        graph.addEventListener('click', function() {
            toggleFullscreen(this); // Pass the clicked element to the function
        });
    });
});